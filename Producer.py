# !/usr/bin/env python
import logging, time
from kafka import KafkaProducer
import numpy as np

class Producer(object):
    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        test = np.loadtxt("/home/ori/PycharmProjects/csv_cleaning/model_data/test.csv",delimiter = ',')
        for row in test:
            try:
                producer.send('my-topic', row.tobytes())
                time.sleep(1)
                print("Producer sent messages!")
            except Exception as e:
                print(e)
                print("Exception occurred, closing producer...")
                producer.close()

        # while True:
        #     try:
        #         msg = input("Enter a message for the consumer: ")
        #         producer.send('my-topic', bytes(msg, 'utf-8'))
        #         print("Producer sent messages!")
        #     except Exception as e:
        #         print(e)
        #         print("Exception occurred, closing producer...")
        #         producer.close()

def main():
    producer = Producer()
    producer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
