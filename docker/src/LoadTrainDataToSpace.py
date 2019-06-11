%pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.getOrCreate()
filePath = "/usr/local/full_train.csv"
df = spark.read.csv(filePath, header=True, inferSchema=True)
df.write.format("org.apache.spark.sql.insightedge").mode("overwrite").save("model.v1.UberRecord")
