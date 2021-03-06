# Amazon MSK

Amazon MSK is a fully managed service that enables you to build and run applications that use Apache Kafka to process streaming data.

## Create MSK Cluster 

- [Via Console](https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html)

- [Via Amazon CDK](https://github.com/wingkwong/aws-playground/tree/master/msk/cdk)

## Create a Client Machine

- Create an EC2 instance to create a topic that produces and consumes data as you cannot access Amazon MSK directly from a local machine. The brokers and zookeeper connect string are private. 

- Download [Apache Kafka](https://kafka.apache.org/downloads)

- Upload to ``~/`` and unzip it. Example: ``~/kafka_2.13-2.6.0/``

- Install ``python3`` by running ``sudo yum install -y python3``

- Install ``java`` by running ``sudo yum install java-1.8.0-openjdk``

- Install ``kafka-python`` by running ``sudo pip install kafka-python``

## Create Kafka Topic

Connect to the client machine

```bash
#!/bin/sh

zookeeperConnectString="<YOUR_ZOOKEEPER_CONNECT_STRING>" # retrieved from "View Client Information" in Amazon MSK Console
kafka_topic="<YOUR_KAFKA_TOPIC>"
replication_factor=1
partitions=1

# Change directory to Kafka bin 
cd ~/kafka_2.13-2.6.0/bin/
# Execute kafka-topics.sh
./kafka-topics.sh --create --zookeeper $zookeeperConnectString --replication-factor $replication_factor --partitions $partitions --topic $kafka_topic
```

## Produce Data

```py
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
```

## Consume Data

```py
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
```

## Streaming data to Amazon S3

Refer to [streaming-data-to-s3.md](https://github.com/wingkwong/aws-playground/blob/master/msk/streaming-data-to-s3.md)

## Common Issues

Thrown the following error while creating a Kafka topic

```
Exception in thread "main" kafka.zookeeper.ZooKeeperClientTimeoutException: Timed out waiting for connection while in state: CONNECTING
    at kafka.zookeeper.ZooKeeperClient.waitUntilConnected(ZooKeeperClient.scala:262)
    at kafka.zookeeper.ZooKeeperClient.<init>(ZooKeeperClient.scala:119)
    at kafka.zk.KafkaZkClient$.apply(KafkaZkClient.scala:1865)
    at kafka.admin.TopicCommand$ZookeeperTopicService$.apply(TopicCommand.scala:360)
    at kafka.admin.TopicCommand$.main(TopicCommand.scala:55)
    at kafka.admin.TopicCommand.main(TopicCommand.scala) 
```

Solution:

Check Securty Group to make sure that the inbound is allowed.