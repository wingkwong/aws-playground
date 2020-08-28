from time import sleep
from json import dumps
from kafka import KafkaProducer

# Define Amazon MSK Brokers
brokers=['<YOUR_MSK_BROKER_1>:9092', '<YOUR_MSK_BROKER_2>:9092']
# Define Kafka topic to be produced to 
kafka_topic='<YOUR_KAFKA_TOPIC>'
# A Kafka client that publishes records to the Kafka cluster
producer = KafkaProducer(bootstrap_servers=brokers, value_serializer=lambda x: dumps(x).encode('utf-8'))
# To produce 1000 numbers from 0 to 999 
for num in range(1000):
    data = {'number' : num}
    producer.send(kafka_topic, value=data)
    sleep(1)
