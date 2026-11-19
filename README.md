# Big Data pipeline in Python: student dropout analytics (2022)

Final assignment for a university e-Government / big-data course (University of Piraeus, submitted July 2022). **Grade: 10/10.**

The course taught the Hadoop ecosystem in **Java**, and all of its instructions and libraries were Java-only. I asked to do the project in **Python** instead. The professor agreed, curious whether I could make it work with no help, so I got no course material or support for that route. I researched both open-source and commercial options for Python (Hadoop Streaming, Confluent's `confluent_kafka` with Avro and Schema Registry, Flume, HDFS, PySpark, MLlib) and taught myself to use them. All of it was written by hand in 2021–22, before AI coding assistants existed.

The one exception is the machine-learning step, which I didn't finish in 2022. It was completed in November 2026 with an AI coding assistant (`mllib_2026.py` and its results page) and is labelled as a 2026 addition everywhere below.

## The problem
The aim is to predict, early in the academic year, whether a university student will drop out, stay enrolled or graduate, so the institution can step in with tutoring or financial support. This is *predictive analytics* with supervised learning on historical student records.

**Dataset:** `student.csv`, 4,424 students with 36 features plus the `Target` label, from *Predict Students' Dropout and Academic Success* (Realinho et al., UCI Machine Learning Repository, 2021, CC BY 4.0).

## Architecture
```
student.csv ──► Kafka producer (Avro + Schema Registry, topic "final_test", 3 partitions)
                     │
                     ▼
               Flume agent "Flafka" ──► 3 memory channels ──► 3 HDFS sinks (Avro, snappy)
                                                                   │
                                                                   ▼
                                        PySpark queries (+ spark-avro) ──► results written back to HDFS as Avro
                                                                   │
                                        Spark MLlib: dropout / enrolled / graduate classifier (finished in 2026)
                                                                   │
                     Flask web UI: one page per stage (start services → Kafka → Spark results → MLlib results)
```
Kafka, ZooKeeper and Schema Registry ran from Confluent's `cp-all-in-one` 7.1.2 Docker Compose stack. Hadoop 3.3.2 (HDFS + YARN), Spark 3.2.1 and Flume 1.9.0 were installed directly on a single-node WSL/Ubuntu machine.

## Files
| Path | What it is |
|---|---|
| `my_files/final_project/topic.py` | creates the Kafka topic through the admin API |
| `my_files/final_project/producer.py` | reads the CSV, casts each field to its type from the Avro schema, and sends Avro records to Kafka |
| `my_files/final_project/student.avsc` | Avro schema for a student record |
| `my_files/twitter.conf` | Flume agent: Kafka source → 3 channels → 3 HDFS sinks (the agent was named during an earlier Twitter exercise) |
| `my_files/twitter_spooldir.conf` | earlier version of the agent: watches a folder and loads CSV files dropped into it |
| `my_files/final_project/spark_map_csv.py` | PySpark queries (admission grade ≥ 160, day vs evening attendance, share of high-admission-grade students in each, students placed in their 1st/2nd choice of programme); results saved to HDFS as Avro |
| `my_files/final_project/spark_map.py` | loads the Avro files that Flume wrote to HDFS into a Spark DataFrame |
| `my_files/final_project/mllib.py` | the 2022 MLlib attempt, unchanged; see Status |
| `my_files/final_project/mllib_2026.py` | **2026 completion** of the MLlib step: scaled features, multinomial logistic regression and a random forest, compared with a majority-class baseline; results in `my_data/mllib_results_2026.txt` and on the UI's last page |
| `my_files/final_project/app.py`, `templates/` | Flask + Bootstrap UI that drives the pipeline step by step |
| `my_files/final_project/start_servers.py`, `avro_data.py` | start Hadoop and the Docker stack; preview raw Avro bytes from HDFS (via `pydoop`) |
| `my_files/hadoop-conf/` | single-node Hadoop config (HDFS on `127.0.0.1:9000`, replication 1, MapReduce on YARN) |
| `my_data/` | real outputs: Flume's Avro files from HDFS, the Spark query results and the MLlib input CSV |
| `my_documentation/documentation.docx`, `my_presentation/presentation.pptx` | report and slides (Greek) |
| [`python-hadoop-streaming/`](python-hadoop-streaming/) | the earlier exercises where I first learned to do the course's MapReduce work in Python |

## Status (what actually ran)
- **Ingestion:** the Avro files in `my_data/final_test_data_*` were written on 2022-07-09 by the folder-watching agent (`twitter_spooldir.conf`); the source CSV in that folder was marked `.COMPLETED` at the same second. The Kafka-source agent was finished later that day. As submitted, it still bound its channels to the old source name `Dir`. That one line was corrected in 2026 (`Flafka.sources.Kafka_src.channels`), and nothing else in it changed.
- **Spark queries:** complete; their outputs are in `my_data/queries/`.
- **MLlib:** not finished in 2022. The report says so: there wasn't time, and the model still had errors. `mllib.py` is kept as it was. It was **completed in 2026** as `mllib_2026.py`, which fixes what blocked it: the label `Target` was also fed in as a feature, `df.na.drop()` was discarded, the non-existent `predictions.accuracy` crashed, and there was no random seed. The 2026 version also adds scaling, a baseline, a random-forest comparison and a Flask results page; the "Start MLlib" button, which in 2022 pointed back to the first page, now leads there.
  Results on a held-out 30% (1,262 students, seed 42): baseline 50.0%, **logistic regression 75.7% accuracy (weighted F1 0.737), random forest 76.5% (F1 0.749)**. Recall: about 73% for Dropout and 94% for Graduate, but only 27–31% for Enrolled, which is the hardest class (it is small and sits between the other two).
- **Code version:** the files in `final_project/` are the copies from the Linux machine where the pipeline ran (recovered in 2026). The Windows-edited submission copy had picked up stray IDE auto-imports, such as `from msilib import schema`, a Windows-only module that fails on Linux.
- **Hard-coded paths:** absolute paths (`/home/nikos/big_data/...`) and the `hdfs://localhost:9000` address are left as they were on the original machine.
- **Hadoop config:** `hdfs-site.xml` sets `dfs.data.dir` twice, where the first entry was presumably meant to be the NameNode directory. Since the later value wins, HDFS still ran.
