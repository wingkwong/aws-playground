"""
spark.py
~~~~~~~~

Module containing helper function for use with Apache Spark
"""

import __main__

from os import environ, listdir, path
import json
from pyspark import SparkFiles
from pyspark.sql import SparkSession

from dependencies import logging


def start_spark(
    app_name="spark-app", master="local[*]", jar_packages=[], files=[], spark_config={}
):
    # detect execution environment
    flag_repl = not (hasattr(__main__, "__file__"))
    flag_debug = "DEBUG" in environ.keys()

    if not (flag_repl or flag_debug):
        # get Spark session factory
        spark_builder = SparkSession.builder.appName(app_name)
    else:
        # get Spark session factory
        spark_builder = SparkSession.builder.master(master).appName(app_name)

        # create Spark JAR packages string
        spark_jars_packages = ",".join(list(jar_packages))
        spark_builder.config("spark.jars.packages", spark_jars_packages)

        spark_files = ",".join(list(files))
        spark_builder.config("spark.files", spark_files)

        # add other config params
        for key, val in spark_config.items():
            spark_builder.config(key, val)

    # create session and retrieve Spark logger object
    spark_sess = spark_builder.getOrCreate()
    spark_logger = logging.Log4j(spark_sess)

    # get config file if sent to cluster with --files
    with open(files[0], "r") as config_file:
        config_dict = json.load(config_file)
    return spark_sess, spark_logger, config_dict
