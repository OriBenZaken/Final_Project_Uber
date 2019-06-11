%pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *

# create pyspark.sql.SparkSession
spark = SparkSession.builder.getOrCreate()

# load SF salaries dataset from file
filePath = "/data/model-data/full_train.csv"
df = spark.read.csv(filePath, header=True, inferSchema=True)
print(df.schema)

# save DataFrame to the grid
df.write.format("org.apache.spark.sql.insightedge").mode("overwrite").save("model.v1.UberRecord")

# load DataFrame from the grid
gridDf = spark.read.format("org.apache.spark.sql.insightedge").option("collection", "model.v1.UberRecord").load()
gridDf.show()
schema = StructType([StructField('latitude',DoubleType(),True),
StructField('longitude',DoubleType(),True),
StructField('base',IntegerType(),True),
StructField('weekday',IntegerType(),True),
StructField('day',IntegerType(),True),
StructField('month',IntegerType(),True),
StructField('year',IntegerType(),True),
StructField('hour',IntegerType(),True),
StructField('isWeekend',IntegerType(),True),
StructField('isHoliday',IntegerType(),True),
StructField('demand',IntegerType(),True)])
# add new row to grid
newRow = spark.createDataFrame([[90000.0, -73.8492, 3, 4, 1, 8, 2014, 17, 1, 1, 75]], schema)
newRow.write.format("org.apache.spark.sql.insightedge").mode("Append").save("model.v1.UberRecord")