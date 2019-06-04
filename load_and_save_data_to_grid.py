%pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import *

# create pyspark.sql.SparkSession
spark = SparkSession.builder.getOrCreate()

# load SF salaries dataset from file
filePath = "/data/model-data/full_train.csv"
#df = spark.read.csv(filePath, header=True, dtype={latitude = 'Double',longitude = 'Double', base = '' })
df = spark.read.csv(filePath, header=True, inferSchema=True)
print(df.schema)

# save DataFrame to the grid
df.write.format("org.apache.spark.sql.insightedge").mode("overwrite").save("model.v1.UberRecord")

# load DataFrame from the grida
#gridDf = spark.read.format("org.apache.spark.sql.insightedge").option("collection", "UberTrainData").load()
#gridDf.show()
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
newRow = spark.createDataFrame([[90000.0, -73.8492, 3, 4, 1, 8, 2014, 17, 1, 1, 75]], schema)
#appended = gridDf.union(newRow)
#appended.show()
#print(appended.count())
newRow.write.format("org.apache.spark.sql.insightedge").mode("Append").save("model.v1.UberRecord")