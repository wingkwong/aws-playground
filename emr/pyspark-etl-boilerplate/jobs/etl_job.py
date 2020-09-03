"""
etl_job.py
~~~~~~~~~~

Usage:

    $SPARK_HOME/bin/spark-submit \
    --master spark://localhost:7077 \
    --py-files packages.zip \
    --files configs/etl_config.json \
    jobs/etl_job.py
"""

import sys
from datetime import datetime
from dependencies.spark import start_spark
from common import df_writer


def main():
    """
    Main ETL script definition.

    :return: None
    """
    platform = sys.argv[1] if len(sys.argv) > 1 else "local"

    if platform not in ["local", "emr"]:
        platform = "local"

    config_path = "./configs/etl_config.json"

    # start Spark application and get Spark session, logger and config
    spark, log, config = start_spark(app_name="spark-app", files=[config_path])

    # log that main ETL job is starting
    log.warn("spark-app is up-and-running")

    if platform == "local":
        spark.sparkContext.addPyFile("jobs/common.py")

    spark.conf.set("spark.sql.crossJoin.enabled", "true")

    # read config
    config = config[platform]

    # execute ETL pipeline

    # extract
    data_frames = extract_data(spark, log, config)

    # transform
    data_frames = transform_data(spark, log, config, data_frames)

    # load
    load_data(spark, log, config, data_frames)

    # log the success and terminate Spark application
    spark.stop()
    return None


def extract_data(spark, log, config):
    """
    Load data from somewhere

    :return: dataframes.
    """
    log.info("*** extract_data starts: {}".format(datetime.now()))
    # LOGIC GOES HERE
    # EXAMPLE
    data_frames = {
        "foo": spark.read.load(
            config["path_data"] + "FILE_NAME",
            format="csv",
            header="false",
            inferSchema="false",
        ),
        "bar": spark.read.load(
            config["path_data"] + "FILE_NAME_1",
            format="csv",
            header="false",
            inferSchema="false",
        ),
        "baz": spark.read.load(
            config["path_data"] + "FILE_NAME_2",
            format="csv",
            header="false",
            inferSchema="false",
        ),
    }
    log.info("*** extract_data ends: {}".format(datetime.now()))

    return data_frames


def transform_data(spark, log, config, data_frames):
    """
    Transform original dataframes.
    
    :return: Transformed dataframes.
    """
    log.info("*** transform_data starts: {}".format(datetime.now()))
    # LOGIC GOES HERE
    log.info("*** transform_data ends: {}".format(datetime.now()))
    return data_frames


def load_data(spark, log, config, data_frames):
    """
    Collect data locally and write to CSV.

    :return: None
    """

    log.info("*** load_data starts: {}".format(datetime.now()))
    # LOGIC GOES HERE
    # EXAMPLE
    df_writer(
        data_frames["foo"],
        file_path="{}/bar".format(config["export_path"]),
        header=True,
        mode="overwrite",
        separator=",",
    )
    log.info("*** load_data ends: {}".format(datetime.now()))
    return None


if __name__ == "__main__":
    """
    Entry point for PySpark ETL application
    """
    main()
