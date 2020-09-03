# PySpark Boilerplate

## Environment Setup 

Download Spark & Hadoop package
```
https://www.apache.org/dyn/closer.lua/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
```

Set environment path

```
set PATH=C:\somewhere\spark-2.4.6-bin-hadoop2.7\bin;%PATH%
```

Install Python 3.7

```
https://www.python.org/downloads/release/python-377/
```

Download ``winutils.exe`` from 

```
https://github.com/steveloughran/winutils/blob/master/hadoop-2.8.1/winutils.exe
```

Save to ``C:\somewhere\hadoop_home\bin``

Set environment path

```
Set HADOOP_HOME=C:\somewhere\hadoop_home
```

## Preferable IDE

Spyder IDE (Install from Anaconda Python distribution)

## Configuration setup

Go to ``/configs``

Copy ``etl_config.json.sample`` and paste it as ``etl_config.json``

update ``etl_config.json``

## Running pipenv

```
pipenv --python 3.6
C:\Users\wingkwong\.virtualenvs\pyspark-etl-boilerplate-XXXXXXXX\Scripts\activate.bat
```

## Submitting Application 

```
nohup spark-submit --py-files packages.zip jobs/etl_job.py 2> output.log &
```

## Code Formatting

```
black target_file.py 
```

## Common issues

Issue: Below error message shows when running spark-submit on Windows 10

```
'Files\spark-2.4.6-bin-hadoop2.7\bin\..\jars""\' is not recognized as an internal or external command,
operable program or batch file.
Failed to find Spark jars directory.
You need to build Spark before running this program.
```

Root Cause: 

The path contains a white space

Solution:

Change 
```
C:\Program Files\spark-2.4.6-bin-hadoop2.7\bin
```

To

``` 
C:\Progra~1\spark-2.4.6-bin-hadoop2.7\bin
```
