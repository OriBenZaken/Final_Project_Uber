# !/usr/bin/env python
import logging
from sklearn.externals import joblib
from kafka import KafkaConsumer, TopicPartition
import numpy as np
from pyspark.sql import SparkSession
import pandas as pd

# run this script with : /gigaspaces-insightedge-enterprise-14.0.0-ga-b20000/insightedge/spark/bin
# need to change the python interpreter of i9e to python 3.5


class Consumer(object):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000,
                                 group_id=None,
                                 enable_auto_commit=True)
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
                        df.write.format("org.apache.spark.sql.insightedge").mode("Append").save("UberTrainData")
                        print("Succeeded write new entry to the data grid")
                    except Exception as e:
                        print("Exception occurred while trying to predict: {}".format(e))
            except Exception as e:
                print("Exception occurred while getting a message from producer: {}".format(e))
                consumer.close()
                break

def convert_np_to_df(spark, np_array):
    df = [float(x) for x in np_array]
    return spark.createDataFrame([df])


def load_model(model_path, testExample=None):
    with open(model_path, 'rb') as f:
        loaded_model = joblib.load(f)
        # if testExample:
        #     test_saved_model(loaded_model, testExample)
        return loaded_model

def main():
    consumer = Consumer()
    consumer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.WARNING
    )
    main()
