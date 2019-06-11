# !/usr/bin/env python
import logging
import time
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
                #model = load_model('/home/ori/PycharmProjects/csv_cleaning/saved_model/rf_uber_model_old.pkl')
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
                            predict_row = np.frombuffer(message.value)
                            try:
                                #pred=model.predict(predict_row.reshape(1, -1))
                                pred=7
                                print(pred)
                                predict_row = np.append(predict_row, pred)
                                df = convert_np_to_df(spark, predict_row)
                                #df.write.format("org.apache.spark.sql.insightedge").mode("Append").save("model.v1.UberRecord")
                                df.write.format("org.apache.spark.sql.insightedge").mode("Append").save(UBER_RECORD_TABLE)
                                print("Kafka Consumer: Succeeded write new entry to the InsightEdge data grid.")
                            except Exception as e:
                                print("Exception occurred while trying to predict: {}".format(e))
                    except Exception as e:
                        print("Exception occurred while getting a message from producer: {}".format(e))
                        consumer.close()
                        break
            except NoBrokersAvailable:
                time.sleep(WAIT_TIME_UNTIL_RETRY_CONNECTION)

def convert_np_to_df(spark, np_array):
    """
    convert numpy to data frame
    :param spark: spark context
    :param np_array: numpy array to be converted
    :return: converted numpy as data frame
    """
    df = [float(x) for x in np_array]
    return spark.createDataFrame([df], UberRecordSchema.schema)


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