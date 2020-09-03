# Amazon Elastic MapReduce (EMR)

```
EEEEEEEEEEEEEEEEEEEE MMMMMMMM           MMMMMMMM RRRRRRRRRRRRRRR
E::::::::::::::::::E M:::::::M         M:::::::M R::::::::::::::R
EE:::::EEEEEEEEE:::E M::::::::M       M::::::::M R:::::RRRRRR:::::R
  E::::E       EEEEE M:::::::::M     M:::::::::M RR::::R      R::::R
  E::::E             M::::::M:::M   M:::M::::::M   R:::R      R::::R
  E:::::EEEEEEEEEE   M:::::M M:::M M:::M M:::::M   R:::RRRRRR:::::R
  E::::::::::::::E   M:::::M  M:::M:::M  M:::::M   R:::::::::::RR
  E:::::EEEEEEEEEE   M:::::M   M:::::M   M:::::M   R:::RRRRRR::::R
  E::::E             M:::::M    M:::M    M:::::M   R:::R      R::::R
  E::::E       EEEEE M:::::M     MMM     M:::::M   R:::R      R::::R
EE:::::EEEEEEEE::::E M:::::M             M:::::M   R:::R      R::::R
E::::::::::::::::::E M:::::M             M:::::M RR::::R      R::::R
EEEEEEEEEEEEEEEEEEEE MMMMMMM             MMMMMMM RRRRRRR      RRRRRR
```

## Sample Boilerplate

```py
from pyspark import SparkContext
from pyspark import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from pyspark.sql.functions import col
from itertools import islice

import sys

if __name__ == '__main__':
    sqlContext = SQLContext(sc)
    # YOUR CODE GOES HERE 
```

## pySpark ETL Boilerplate

https://github.com/wingkwong/aws-playground/tree/master/emr/pySpark-etl-boilerplate/

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


## Update Configuration Object

```json
[
     {
      "InstanceGroupId":"ig-1XXXXXXXXXXX9",
      "Configurations": []
   }
]
```

Then run

```
aws emr modify-instance-groups --cluster-id j-1XXXXXXXXXXX9 --instance-groups file://new-configuration-object.json
```

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
df = spark.read.<format method>.("filename.<format>")
```

Replace 0 to null
```py
df = df.withColumn('COL1', when(df['COL1'] == 0, 'null').otherwise(df['COL1']))
```

Combine columns
```py
df = df.withColumn('NEW_COL', concat(df['COL1'], lit("-"),df['COL2'], lit("-")))
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

## UDF

```python
def your_python_func(a,b,c,d,e,f):
    # Your logic goes here
    return ""

your_udf = udf(lambda a,b,c,d,e,f: your_python_func(a,b,c,d,e,f))

# Add a new column called NEW_COLUMN_NAME
df = df.withColumn("NEW_COLUMN_NAME", your_udf(
                        df.a,       # a must be found in df
                        df.b,       # b must be found in df
                        df.c,       # c must be found in df
                        df.d,       # d must be found in df
                        lit('e'),   # use lit for non-column parameters
                        lit('f')    # use lit for non-column parameters
                    )
                )
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

## Notebook

Dataset Source: https://dj2taa9i652rf.cloudfront.net/

```
aws s3 ls s3://covid19-lake/safegraph-open-census-data/csv/data/
2020-04-14 16:00:26    5853188 cbg_b00.csv
2020-04-14 16:00:27  103987464 cbg_b01.csv
2020-04-14 16:00:26   49434240 cbg_b02.csv
2020-04-14 16:00:26   35330595 cbg_b03.csv
2020-04-14 16:00:27   67026929 cbg_b07.csv
2020-04-14 16:00:29  348314677 cbg_b08.csv
2020-04-14 16:00:26  154882703 cbg_b09.csv
2020-04-14 16:00:59  401362335 cbg_b11.csv
2020-04-14 16:00:25   30214746 cbg_b12.csv
2020-04-14 16:00:29  319142985 cbg_b14.csv
2020-04-14 16:00:29  214808873 cbg_b15.csv
2020-04-14 16:00:29  295345041 cbg_b19.csv
2020-04-14 16:00:27   86140098 cbg_b20.csv
2020-04-14 16:00:36  117175299 cbg_b21.csv
2020-04-14 16:00:26   12906267 cbg_b22.csv
2020-04-14 16:00:30  418569641 cbg_b23.csv
2020-04-14 16:00:26 1095818025 cbg_b25.csv
2020-04-14 16:00:27   85605814 cbg_b27.csv
2020-04-14 16:00:32  390135948 cbg_b99.csv
2020-04-14 16:00:28   99341995 cbg_c16.csv
2020-04-14 16:00:27  187799316 cbg_c17.csv
2020-04-14 16:00:35  411225125 cbg_c24.csv
```

```python
spark.read.csv("s3://covid19-lake/safegraph-open-census-data/csv/data/cbg_b23.csv").count()
```

![image](https://user-images.githubusercontent.com/35857179/84880417-0f4a6f80-b0bf-11ea-8f02-77c370bd4cc5.png)

### Common Issues

- Failed to start a Notebook. Notebook is stopped. Service Role does not have the required permissions.

    Make sure the role has ``AmazonElasticMapReduceEditorsRole`` policy. The default managed policy attached to ``EMR_Notebooks_DefaultRole`` is ``AmazonElasticMapReduceEditorsRole``. 

- Failed to start Notebook Kernel. Error attempting to connect to Gateway server url 'http://localhost:17777'. Ensure gateway url is valid and the Gateway instance is running."

    There seems to be an issue with 5.30.0. It works fine in 5.29.0. (As of 17/06/2020)

# Lession Learned

- Parentheses are required for multiple conditions in filter

    ```
    df.filter(
        (col("COL1") == a)
        & (col("COL2") == b)
        & (col("COL3") == c)
        & (col("COL4") == d)
    )
    ```

- You cannot pass dataframes into a UDF because they live in the spark context and they are only available as such inside the driver. Try to serialize it and broadcast it.

- Using UDFs is kind of slow

- Don't use much for-loop 

- Pivot with agg

    ```py
    df.groupBy(["A", "B"])
    .pivot("X")
    .agg(
        first("C").alias("D"),
    )
    ```

    Expected to see 

    ```
    ['A',
    'B',
    '0_D',
    '1_D',
    '2_D',
    '3_D',
    '4_D']
    ```

    But it got 

    ```py
    ['A', 'B', '0', '1', '2', '3', '4']
    ```

    Sol: add a dummy column

    ```py
        df.groupBy(["A", "B"])
        .pivot("X")
        .agg(
            first("C").alias("D"),
            first(lit("")).alias("DUMMY"),
        )
    ```

    ```
    ['A',
    'B',
    '0_D',
    '0_DUMMY',
    '1_D',
    '1_DUMMY',
    '2_D',
    '2_DUMMY',
    '3_D',
    '3_DUMMY',
    '4_D',
    '4_DUMMY']
    ```
- Python Version

    Amazon EMR release versions 4.6.0-5.19.0: Python 3.4 is installed on the cluster instances. Python 2.7 is the system default.
    
    Amazon EMR release versions 5.20.0 and later: Python 3.6 is installed on the cluster instances. Python 2.7 is the system default.

    Add a configuration object similar to the following when you launch a cluster using Amazon EMR release version 4.6.0 or later:

    ```json
    [
    {
        "Classification": "spark-env",
        "Configurations": [
        {
            "Classification": "export",
            "Properties": {
                "PYSPARK_PYTHON": "/usr/bin/python3"
            }
        }
        ]
    }
    ]
    ```
- Use Ganglia to see the metrics and gain insights for performance tuning 


# Useful links 
- [Registry of Open Data on AWS](https://registry.opendata.aws/amazon-reviews/)
- [Python For Data Science Cheat Sheet: PySpark - SQL Basics](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PySpark_SQL_Cheat_Sheet_Python.pdf)