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
    