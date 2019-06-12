# !/usr/bin/env python
import logging
import time
from sklearn import externals
from sklearn.externals import joblib
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd


###############################################
######### UberRecord Schema Class #############
###############################################

class UberRecordSchema(object):
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

# run this script with : /gigaspaces-insightedge-enterprise-14.0.0-ga-b20000/insightedge/spark/bin/spark-submit
# need to change the python interpreter of i9e to python 3.5

WAIT_TIME_UNTIL_RETRY_CONNECTION = 10 # In seconds
UBER_RECORD_TABLE = "model.v1.UberRecord"

###############################################
########### Kafka Consumer Class ##############
###############################################

class Consumer(object):
    def run(self):
        """
        run function.
        runs the consumer code. gets queries from producer and uses the traines model in order to predict demand.
        """
        while True:
            try:
                print("Kafka Consumer: Trying to establish connection to kafka server...")
                consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                         auto_offset_reset='earliest',
                                         consumer_timeout_ms=1000,
                                         group_id=None,
                                         enable_auto_commit=True)
                print("Kafka Consumer: Succeeded to establishe connection to kafka server.")
                model = load_model('/data/final_model.joblib')
                topic = 'my-topic-2'
                consumer.topics()
                # create pyspark.sql.SparkSession
                spark = SparkSession.builder.getOrCreate()
                partitions = consumer.partitions_for_topic(topic)
                if partitions is not None:
                    for p in partitions:
                        assignments = [TopicPartition(topic, p)]
                    consumer.assign(assignments)
                    # start iterate
                    consumer.seek_to_end()
                else:
                    consumer.subscribe([topic])
                while True:
                    try:
                        for message in consumer:
                            str_msg = message.value.decode()
                            to_predict_row_as_np = get_nparray_ride_info_from_string(str_msg)
                            try:
                                pred=model.predict(to_predict_row_as_np.reshape(1, -1))
                                print("Model demand prediction for ride info: {} is {}".format(str_msg, pred))
                                newRow = spark.createDataFrame([get_list_from_string(str_msg) + [pred]],  UberRecordSchema.schema)
                                newRow.write.format("org.apache.spark.sql.insightedge").mode("Append").save(UBER_RECORD_TABLE)
                                print("Kafka Consumer: Succeeded write new entry to the InsightEdge data grid.")
                            except Exception as e:
                                print("Exception occurred while trying to predict: {}".format(e))
                    except Exception as e:
                        print("Exception occurred while getting a message from producer: {}".format(e))
                        consumer.close()
                        break
            except NoBrokersAvailable:
                time.sleep(WAIT_TIME_UNTIL_RETRY_CONNECTION)

def convert_string_to_df(spark, np_array):
    """
    convert numpy to data frame
    :param spark: spark context
    :param np_array: numpy array to be converted
    :return: converted numpy as data frame
    """
    df = [float(x) for x in np_array]
    return spark.createDataFrame([df], UberRecordSchema.schema)

def get_list_from_string(ride_info_string):
    ride_info = ride_info_string.split(",")
    ride_info = [data.strip() for data in ride_info]
    ride_info = [int(data) if i>=2 else float(data) for i,data in enumerate(ride_info)]
    return  ride_info

def get_nparray_ride_info_from_string(ride_info_string):
    """
    split given string
    :param ride_info_string: input query string
    :return: numpy array
    """
    ride_info = get_list_from_string(ride_info_string)
    return np.asarray(ride_info)

def load_model(model_path):
    """
    the function loads the model
    :param model_path: model path
    :return: the loaded model
    """
    with open(model_path, 'rb') as f:
        loaded_model = joblib.load(f)
        return loaded_model

def main():
    """
    main function, runs the program.
    """
    consumer = Consumer()
    consumer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.CRITICAL
    )
    main()