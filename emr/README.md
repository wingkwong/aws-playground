# Amazon Elastic MapReduce (EMR)

## Create cluster with step

After running below command, you should see your EMR Cluster ID. 

```bash
aws emr create-cluster --name "Spark cluster with step" \
    --release-label emr-5.24.1 \
    --applications Name=Spark \
    --log-uri s3://your-bucket/logs/ \
    --ec2-attributes KeyName=your-key-pair \
    --instance-type m5.xlarge \
    --instance-count 3 \
    --bootstrap-actions Path=s3://your-bucket/bootstrap.sh \
    --steps Type=Spark,Name="Spark job",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,s3://your-bucket/pyspark_job.py] \
    --use-default-roles \
    --auto-terminate
```

## Create a new step to an existing cluster

```
aws emr add-steps --cluster-id <Your EMR Cluster ID> --steps Type=spark,Name=TestJob,Args=[--deploy-mode,cluster,--master,yarn,--conf,spark.yarn.submit.waitAppCompletion=true,s3a://your-bucket/code/pyspark_job2.py,s3a://your-source-bucket/data/data.csv,s3a://your-destination-bucket/test-output/],ActionOnFailure=CONTINUE
```

## S3 Paths

- ``s3:\\``: s3 which is also called classic (s3: filesystem for reading from or storing objects in Amazon S3 This has been deprecated and recommends using either the second or third generation library.
- ``s3n:\\``: s3n uses native s3 object and makes easy to use it with Hadoop and other files systems. This is also not the recommended option.
- ``s3a:\\``: s3a – This is a replacement of s3n which supports larger files and improves in performance.


## Pyspark Code Snippets

Read a CSV file, split by commas, and store it an RDD
```py
rdd = sc.textFile('s3n://your-bucket/test.csv').map(lambda line: line.split(','))
```

RDD to DF
```py
df = rdd.toDF(['COL1', 'COL2', 'COL3', 'COL4'])
```

Read a CSV file to DF

```py
# Reading a CSV
df = spark.read.csv("filename.csv")

# Reading a CSV with header
df = spark.read.csv("filename.csv", header=True)

# Reading a CSV using the load method
df = spark.read.format("csv").load("filename.csv")

# Reading a CSV using the load method with header
df = spark.read.format("csv").option("header", "true").load("filename.csv")

# The same goes for different formats
df = spark.read.format("<file format>").load("filename.<format>")

# Or using the given method
df = spark.read.<format method>.("filename.<format>)
```

Replace 0 to null
```py
df = df.withColumn('COL1', when(df['COL1'] == 0, 'null').otherwise(df['COL1']))
```

Filtering
```py
# Filter your DataFrame with non-null values
df = df.filter(df.column1 != 'null')

# Filter your DataFrame and select a column
df.filter(df.column1 > 20).select("column2").show()

# Filter your DataFrame with AND
df.filter((df.column1 > 20) & (df.column2 < 10)).select("column2").show()

# Filter your DataFrame with OR
df.filter((df.column1 > 20) | (df.column2 < 10)).select("column2").show()
```

GroupBy 
```py
# GroupBy a column and count
df.groupby("column").count().show()

# GroupBy a column and sum
df.groupby("column1").sum("column2").show()

# GroupBy with multiple columns
df.groupby("column1", "column2").count().show()

# GroupBy with multiple columns and sum multiple columns
df.groupby("column1", "column2").sum("column3", "column4").show()
```

Write back to s3 

```py
# save in parquet format
df.write.parquet('s3a://your-bucket/test.parquet')
# save with header 
df.write.option("header","true").parquet('s3a://your-bucket/test.parquet')
# save in csv format
df.write.csv("s3a://your-bucket/test.csv")
```

## View Log Files

### View Log Files on the Master Node
- ``/mnt/var/log/bootstrap-actions``: Logs written during the processing of the bootstrap actions.
- ``/mnt/var/log/hadoop-state-pusher``: Logs written by the Hadoop state pusher process.
- ``/mnt/var/log/instance-controller (Amazon EMR 4.6.0 and earlier)`` : Instance controller logs.
- ``/emr/instance-controller (Amazon EMR 4.7.0 and later)``: Instance controller logs.
- ``/mnt/var/log/instance-state``: Instance state logs. These contain information about the CPU, memory state, and garbage collector threads of the node.
- ``/mnt/var/log/service-nanny (Amazon EMR 4.6.0 and earlier)``: Logs written by the service nanny process.
- ``/emr/service-nanny (Amazon EMR 4.7.0 and later)``: Logs written by the service nanny process.
- ``/mnt/var/log/application``: Logs specific to an application such as Hadoop, Spark, or Hive.
- ``/mnt/var/log/hadoop/steps/N``: Step logs that contain information about the processing of the step. The value of N indicates the stepId assigned by Amazon EMR. For example, a cluster has two steps: s-1234ABCDEFGH and s-5678IJKLMNOP. The first step is located in /mnt/var/log/hadoop/steps/s-1234ABCDEFGH/ and the second step in /mnt/var/log/hadoop/steps/s-5678IJKLMNOP/.

Use SSH to connect to the master node

```bash
# Navigate to the directory that contains the log file information you wish to view.
cd /mnt/var/log/hadoop/steps/s-1234ABCDEFGH/
# Use a file viewer of your choice to view the log file.
less controller
```

### View Log Files Archived to Amazon S3

By default, Amazon EMR clusters launched using the console automatically archive log files to Amazon S3. Log files are uploaded to Amazon S3 every 5 minutes. 

- /``JobFlowId``/node/
- /``JobFlowId``/node/``instanceId``/``application``
- /``JobFlowId``/steps/``N``/

### View Log Files in the Debugging Tool

Amazon EMR does not automatically enable the debugging tool. You must configure this when you launch the cluster.

To view cluster logs, 

Open the Amazon EMR console -> Select Cluster -> Select View Jobs -> Select View Tasks -> Select View Attempts -> Choose stderr, stdout, and syslog

## Accessing the Spark Web UIs

You can also navigate to the Spark HistoryServer UI directly at ``http://master-public-dns-name:18080/``

# Useful links 
- [Registry of Open Data on AWS](https://registry.opendata.aws/amazon-reviews/)
- [Python For Data Science Cheat Sheet: PySpark - SQL Basics](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PySpark_SQL_Cheat_Sheet_Python.pdf)