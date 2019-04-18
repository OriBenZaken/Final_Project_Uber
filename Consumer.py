# !/usr/bin/env python
import threading, logging, time
import multiprocessing
from sklearn.externals import joblib
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import numpy as np


class Consumer(object):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000,
                                 group_id=None,
                                 enable_auto_commit=True)
        model = load_model('/home/ori/PycharmProjects/csv_cleaning/saved_model/rf_uber_model.pkl')
        topic = 'my-topic'
        partitions = consumer.partitions_for_topic(topic)
        for p in partitions:
            assignments = [TopicPartition(topic, p)]
        consumer.assign(assignments)
        # start iterate
        consumer.seek_to_end()
        while True:
            try:
                for message in consumer:
                    predict_row = np.frombuffer(message.value, dtype = np)
                    print("Got message from producer: {}".format(predict_row))
                    print (model.predict(predict_row)) #need to to convers
            except Exception as e:
                print(e)
                print("Exception occurred, closing consumer...")
                consumer.close()

def load_model(model_path, testExample=None):
    with open(model_path, 'rb') as f:
        loaded_model = joblib.load(f)
        # if testExample:
        #     test_saved_model(loaded_model, testExample)

def main():
    consumer = Consumer()
    consumer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
