#!/bin/sh

zookeeperConnectString="<YOUR_ZOOKEEPER_CONNECT_STRING>" # retrieved from "View Client Information" in Amazon MSK Console
kafka_topic="<YOUR_KAFKA_TOPIC>"
replication_factor=1
partitions=1

# Change directory to Kafka bin 
cd /home/ec2-user/kafka_2.13-2.6.0/bin/
# Execute kafka-topics.sh
./kafka-topics.sh --create --zookeeper $zookeeperConnectString --replication-factor $replication_factor --partitions $partitions --topic $kafka_topic