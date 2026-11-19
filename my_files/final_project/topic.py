from confluent_kafka.admin import AdminClient, NewTopic

# create admin client
ac = AdminClient({"bootstrap.servers": "localhost:9092"})

# create topic
topic = NewTopic("final_test", num_partitions = 3, replication_factor = 1)
ac.delete_topics([topic])
ac.create_topics([topic])