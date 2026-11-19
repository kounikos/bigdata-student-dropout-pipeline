# This resolves pyspark python path issues
import findspark
findspark.init()

from confluent_kafka.avro import AvroConsumer

from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder\
    .appName("spark_map")\
        .master("local[*]")\
        .config("spark.jars", "/home/nikos/big_data/python_programs/final_project/jars/spark-avro_2.12-3.2.1.jar")\
        .getOrCreate()

# Load schema file into StructType
schema = open("/home/nikos/big_data/python_programs/final_project/student.avsc", "r").read()



# Load data from hdfs folders into DataFrame
try :
    df = spark.read.format("avro")\
        .options(avroSchema = schema)\
        .load("hdfs://localhost:9000/final_test_data_1/")
except Exception as e:
    print(e)
# df = spark.read.format("avro")\
#     .load(["hdfs://localhost:9000/final_test_data_1/", \
#     "hdfs://localhost:9000/final_test_data_2/", "hdfs://localhost:9000/final_test_data_3/"])\    

# save the dataframe to an avro file
df.write.format("avro").save("hdfs://localhost:9000/spark_avro/")

# Print the schema
# df.show(n=2, vertical=True)
