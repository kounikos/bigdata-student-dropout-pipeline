def kafka_job():
    from confluent_kafka import avro
    from confluent_kafka.avro import AvroProducer

    import csv
    import json

    
    # load the schema for the avro schema
    value_schema = avro.load("/home/nikos/big_data/python_programs/final_project/student.avsc")

    # Configure the Kafka Producer
    AvroProducerConf = {"bootstrap.servers": "localhost:9092",
                        "schema.registry.url": "http://localhost:8081"
                        }

    # Create the producer
    producer = AvroProducer(AvroProducerConf, default_value_schema=value_schema)

    data_type = dict()
    #Parse the schema to get the datatype of each column
    with open("/home/nikos/big_data/python_programs/final_project/student.avsc") as json_file:
        json = json.load(json_file)
        for fields in json['fields']:
            if len(fields['type'][0]) > 1:
                data_type[fields['name']] = fields['type'][0]
            else:
                data_type[fields['name']] = fields['type']

    # Read the csv file
    with open("/home/nikos/big_data/python_programs/final_project/student.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        headers = reader.fieldnames
        for row in reader:
            for header in headers:
                if data_type[header] == 'string':
                    row[header] = str(row[header])
                elif data_type[header] == 'int':
                    row[header] = int(row[header])
                elif data_type[header] == 'float':
                    row[header] = float(row[header])
                else:
                    raise("Unknown data type")
            # Send the data to Kafka
            producer.produce(topic = "final_test", value = row)
            producer.flush()