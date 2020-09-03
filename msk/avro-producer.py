from time import sleep
from json import dumps
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define Amazon MSK Brokers
brokers='<YOUR_MSK_BROKER_1>,<YOUR_MSK_BROKER_2>'
# Define Schema Registry
schema_registry='<YOUR_SCHEMA_REGISTRY>'
# Define Kafka topic to be produced to 
kafka_topic='<YOUR_KAFKA_TOPIC>'
# Value Schema
value_schema_str = """
{
   "type":"record",
   "name":"value_schema",
   "fields":[
      {
         "name":"id",
         "type":[
            "null",
            "int"
         ],
         "default":null
      }
   ]
}
"""
# Key Schema
key_schema_str = """
{
   "type":"record",
   "name":"key_schema",
   "fields":[
      {
         "name":"id",
         "type":"int"
      }
   ]
}
"""

def delivery_report(err, msg):
    """ 
        Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). 
    """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)
key = {"id": 1}
avroProducer = AvroProducer({
    'bootstrap.servers': brokers,
    'on_delivery': delivery_report,
    'schema.registry.url': schema_registry
}, default_key_schema=key_schema, default_value_schema=value_schema)
avroProducer.produce(topic=kafka_topic, key=key)
avroProducer.flush()