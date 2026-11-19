# Python on Hadoop: the exercises behind the final project (Apr–Jun 2022)

The course's lab exercises were written in Java against the Hadoop MapReduce API (see [`../../tier2-bigdata-java/`](../../tier2-bigdata-java/)). Here the author redid them in Python using **Hadoop Streaming**: mappers and reducers are plain scripts that read stdin and write tab-separated key/value pairs, run on HDFS + YARN through `hadoop-streaming-3.3.2.jar`. Each one was first tested locally with `cat data | python3 mapper.py | sort | python3 reducer.py`, then submitted to the cluster.

| Folder | Job |
|---|---|
| `word-count/` | counts weather keywords (`weather`, `forecast`, `rainy`, …) in text (the first streaming job). `reducer.py` still uses Python 2 `print`; the `_3` variants are Python 3. |
| `weather/` | four MapReduce jobs over daily weather records (`weather_1.csv`, `weather_2.csv`; MinTemp … RainTomorrow): (a) how many days are followed by rain, (b) how often each rainfall value occurs, (c) how often each max-temperature value occurs, (d) days grouped into 10–20 / 21–30 / 31–40 bands. Job (d) was meant to average min and max temperature, but it reads columns 1 and 2 (MaxTemp and Rainfall), an off-by-one left as written. Includes the `hadoop jar` runner. |
| `flafka-keyword-count/` | the keyword count run on data that Flume had loaded into HDFS (`/Flafka_weather_data`), the first Kafka → Flume → HDFS → MapReduce chain |
| `kafka-twitter/producer.py` | a Tweepy streaming client that sends keyword-filtered tweets to a Kafka topic. **The API credentials are redacted**; the originals from 2022 should be considered exposed and revoked. |
| `kafka-twitter/employee.avsc` | first Avro schema exercise |
| `start_servers.py` | starts Hadoop, ZooKeeper and Kafka from Python (later reused in the final project) |

These files come from the original WSL machine (`~/big_data/python_programs/`), recovered in 2026. The shell history on that machine confirms the workflow: `hdfs dfs -mkdir/-copyFromLocal`, local pipe tests, then `hadoop jar … -mapper … -reducer …`.
