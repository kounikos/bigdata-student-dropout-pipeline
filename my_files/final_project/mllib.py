import findspark
findspark.init()

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder\
    .appName("multiclass_classification")\
    .master("local[*]")\
    .config("spark.jars", "/home/nikos/big_data/python_programs/final_project/jars/spark-avro_2.12-3.2.1.jar")\
    .getOrCreate()

# # Load data from hdfs folder deserialized to DataFrame
# df = spark.read.format("avro")\
#     .load("/queries/students.avro")
# df.write.format("csv").mode("overwrite").save("/queries/students.csv", header=True)
# df = spark.read.format("csv")\
#     .load("/queries/students.csv", header=True, InferSchema=True)

# Load csv file to DataFrame
df = spark.read.format("csv")\
    .load("/mLlib_csv/student_mLlib.csv", header=True, InferSchema=True)

# Make sure no missing values
df.na.drop()

# Preprocess data
assembler = VectorAssembler(outputCol="features", inputCols=df.columns[::])
output_data = assembler.transform(df)
final_data = output_data.select("features", "Target")

# Split data into training and testing sets
train, test = output_data.randomSplit([0.7, 0.3])
# Train the model
model = LogisticRegression(labelCol="Target", featuresCol="features", family="multinomial", numClasses=3)
trained = model.fit(train)
# Evaluate the model
predictions = trained.transform(test)
predictions.show()
print("Accuracy: %2.2f%%" % (predictions.accuracy * 100.0))
# Print the results

