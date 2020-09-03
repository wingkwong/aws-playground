# Streaming Data to S3

There is not a direct way to stream data to Amazon S3. You need a S3 Connector. The following demostration is performed in ``ap-east-1`` region and the Apache Kafka version is ``2.2.1``.

## Prerequisites

You should have 

- MSK Cluster
- Apache Kafka topic
- Producer 
- S3 bucket

## Installation

Since we are not using Confluent Cloud, we need to download and install it manually.

Go to [https://www.confluent.io/hub/confluentinc/kafka-connect-s3](https://www.confluent.io/hub/confluentinc/kafka-connect-s3) to download Kafka Connect S3

Extract the ZIP file contents and copy the contents to the desired location. For example, you can create a directory named ``/home/ec2-user/kafka-plugins`` then copy the connector plugin contents.

## Configuration

Add this to the plugin path in your Connect properties file  ``connect.properties``

```
plugin.path=/home/ec2-user/kafka-plugins/
```

Update ``bootstrap.servers`` 

```
bootstrap.servers=X-X.XXXXXXXXXXX-XX.XXXXXX.XX.kafka.ap-east-1.amazonaws.com:9092,X-X.XXXXXXXXXXX-XX.XXXXXX.XX.kafka.ap-east-1.amazonaws.com:9092
```

Update ``topic``

```
topic=<YOUR_KAFKA_TOPIC>
```

Define desired converter key and value. By default the value is empty, if you don't specify them, you will get ``JDBC Sink: JsonConverter with schemas.enable requires "schema" and "payload" fields and may not contain additional fields.`` error. 

```
key.converter=org.apache.kafka.connect.storage.StringConverter
key.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.storage.StringConverter
value.converter.schemas.enable=false
```

If you want to convert the data to parquet format. You must use the AvroConverter with ParquetFormat. Attempting to use other Converter will result in a runtime exception.

```
key.converter=io.confluent.connect.avro.AvroConverter
key.converter.schema.registry.url=http://10.0.0.0:8081
value.converter=io.confluent.connect.avro.AvroConverter
value.converter.schema.registry.url=http://10.0.0.0:8081
```

Then, define sink connector properties. A sample properties file is available under ``etc/`` in the zip. 

```
name=s3-sink
connector.class=io.confluent.connect.s3.S3SinkConnector
tasks.max=1
topics=<YOUR_KAFKA_TOPIC>

s3.region=ap-east-1
s3.bucket.name=<YOUR_BUCKET>
s3.part.size=5242880
flush.size=1

storage.class=io.confluent.connect.s3.storage.S3Storage
format.class=io.confluent.connect.s3.format.avro.AvroFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner

schema.compatibility=NONE
```

With ``flush.size`` > 1 and ``value.converter`` = ``JsonConverter`` , you may get ``org.apache.avro.AvroRuntimeException: already open`` error. 

In order to contacting S3 successfully, you need to provide AWS credentials to authenticate for the S3 connector.

```
export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=bar
```

## Producing the data

Here's a sample producer

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

Start to produce data to the topic
```
python3 ./producer.py
```

## Streaming data to S3

Run 

```
~/kafka_2.13-2.6.0/bin/connect-standalone.sh ~/kafka-plugins/confluentinc-kafka-connect-s3-5.5.1/etc/connector.properties ~/kafka-plugins/confluentinc-kafka-connect-s3-5.5.1/etc/s3-sink.properties
```

## Result

You should see those objects with keys:

```
topics/<YOUR_KAFKA_TOPIC>/partition=0/<YOUR_KAFKA_TOPIC>+0+0000000000.avro
topics/<YOUR_KAFKA_TOPIC>/partition=0/<YOUR_KAFKA_TOPIC>+0+0000000001.avro
topics/<YOUR_KAFKA_TOPIC>/partition=0/<YOUR_KAFKA_TOPIC>+0+0000000002.avro
...
```

![image](https://user-images.githubusercontent.com/35857179/91855683-13d2fd00-ec98-11ea-8172-3034e7215ed3.png)

Download the first one verify. You can either use Avor Viewer to view it and export it as json

```json
[
  {
    "boolean": null,
    "bytes": null,
    "double": null,
    "float": null,
    "int": null,
    "long": null,
    "string": null,
    "array": null,
    "map": [
      {
        "key": {
          "boolean": null,
          "bytes": null,
          "double": null,
          "float": null,
          "int": null,
          "long": null,
          "string": "number",
          "array": null,
          "map": null
        },
        "value": {
          "boolean": null,
          "bytes": null,
          "double": null,
          "float": null,
          "int": null,
          "long": 0,
          "string": null,
          "array": null,
          "map": null
        }
      }
    ]
  }
]
```

or use ``avro-tools-1.7.7.jar`` ([download here](http://mirror.metrocast.net/apache/avro/avro-1.7.7/java/avro-tools-1.7.7.jar)) to convert it back to json

```
java -jar avro-tools-1.7.7.jar tojson <YOUR_KAFKA_TOPIC>+0+0000000000.avro
```

```json
{"number":0}
```

If you want multiple records inside one .avro file, increase the value of ``flush.size``.

## Common issues

NoClassDefFoundError is thrown when using ``io.confluent.connect.s3.format.parquet.ParquetFormat ``

`` java.lang.NoClassDefFoundError: com/google/common/base/Preconditions`` 

Solution

Download the missing jar [guava-17.0.jar](https://www.findjar.com/jar/com/google/guava/guava/17.0/guava-17.0.jar.html) and add it back to ``/lib``

## Useful links

- [Amazon S3 Sink Connector for Confluent Platform](https://docs.confluent.io/current/connect/kafka-connect-s3/index.html)
- [Avor Viewer](https://zymeworks.github.io/avro-viewer/)