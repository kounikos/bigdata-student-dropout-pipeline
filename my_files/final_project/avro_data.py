import pydoop.hdfs as hdfs


# This loads the data from the avro file into a string
def load_avro_data():
    with hdfs.open("hdfs://localhost:9000/final_test_data_2/FlumeData.1657358953133", "rb") as f:
        avro_data = f.read(1200)
    return str(avro_data)
    