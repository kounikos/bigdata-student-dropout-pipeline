"""Student outcome classification with Spark MLlib (completed in 2026).

The 2022 attempt (mllib.py, kept unchanged) never ran to the end. This version
finishes it with the same idea, a multinomial logistic regression over the
student features, and fixes what stopped the original:
  * the label column `Target` was also fed in as a feature (label leakage)
  * `df.na.drop()` returned a new DataFrame that was thrown away
  * `predictions.accuracy` does not exist, so evaluation crashed
  * no fixed random seed, so results were not reproducible
It adds feature scaling, a majority-class baseline and a random-forest
comparison, and it reports accuracy, weighted F1, per-class recall and a
confusion matrix.

Run on its own:  python3 mllib_2026.py [path/to/student_mLlib.csv]
Or from the Flask app (app.py -> /mllib_results), which calls ml_job().
"""
import os
import sys

import findspark
findspark.init()

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StandardScaler, VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "student_mLlib.csv")
LABELS = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}  # encoding used in student_mLlib.csv
SEED = 42


def ml_job(csv_path=DEFAULT_CSV):
    spark = SparkSession.builder\
        .appName("student_outcome_classification")\
        .master("local[*]")\
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # Load the preprocessed CSV (all columns numeric, Target already encoded 0/1/2)
    df = spark.read.csv("file://" + os.path.abspath(csv_path), header=True, inferSchema=True)
    df = df.na.drop().withColumn("label", F.col("Target").cast("double"))

    feature_cols = [c for c in df.columns if c not in ("Target", "label")]
    train, test = df.randomSplit([0.7, 0.3], seed=SEED)
    train.cache()

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
    scaler = StandardScaler(inputCol="raw_features", outputCol="features", withMean=True, withStd=True)
    models = {
        "Logistic regression (multinomial)": LogisticRegression(
            family="multinomial", maxIter=200, regParam=0.01, elasticNetParam=0.0),
        "Random forest (100 trees)": RandomForestClassifier(numTrees=100, maxDepth=10, seed=SEED),
    }

    accuracy = MulticlassClassificationEvaluator(metricName="accuracy")
    f1 = MulticlassClassificationEvaluator(metricName="f1")

    results = [
        f"Dataset: {df.count()} students, {len(feature_cols)} features; "
        f"train {train.count()} / test {test.count()} (70/30 split, seed {SEED})"
    ]

    # Baseline: always predict the most common class seen in training
    majority = train.groupBy("label").count().orderBy(F.desc("count")).first()["label"]
    baseline_acc = test.filter(F.col("label") == majority).count() / test.count()
    results.append(f"Baseline (always '{LABELS[int(majority)]}'): accuracy {baseline_acc:.1%}")

    for name, clf in models.items():
        model = Pipeline(stages=[assembler, scaler, clf]).fit(train)
        predictions = model.transform(test).cache()

        acc = accuracy.evaluate(predictions)
        f1_score = f1.evaluate(predictions)
        results.append(f"{name}: accuracy {acc:.1%}, weighted F1 {f1_score:.3f}")

        # Per-class recall and confusion matrix (rows = actual, columns = predicted)
        counts = {(int(r["label"]), int(r["prediction"])): r["count"]
                  for r in predictions.groupBy("label", "prediction").count().collect()}
        recalls = []
        for actual, label_name in LABELS.items():
            total = sum(counts.get((actual, p), 0) for p in LABELS)
            hit = counts.get((actual, actual), 0)
            recalls.append(f"{label_name} {hit / total:.0%}" if total else f"{label_name} n/a")
        results.append(f"  recall per class: {', '.join(recalls)}")
        header = "  confusion (actual \\ predicted): " + " | ".join(LABELS.values())
        rows = [f"    {LABELS[a]:>8}: " + " | ".join(str(counts.get((a, p), 0)) for p in LABELS) for a in LABELS]
        results.append("\n".join([header] + rows))

    spark.stop()
    return results


if __name__ == "__main__":
    for line in ml_job(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV):
        print(line)
