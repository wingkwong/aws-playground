from kafka import KafkaConsumer
from json import loads

# Define Amazon MSK Brokers
brokers=['<YOUR_MSK_BROKER_1>:9092', '<YOUR_MSK_BROKER_2>:9092']
# Define Kafka topic to be consumed from 
kafka_topic='<YOUR_KAFKA_TOPIC>'
# A Kafka client that consumes records from a Kafka cluster
consumer = KafkaConsumer(
          kafka_topic,
          bootstrap_servers=brokers,
          auto_offset_reset='earliest',
          enable_auto_commit=True,
          group_id='my-group',
          value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
          message = message.value
          print('{}'.format(message))
