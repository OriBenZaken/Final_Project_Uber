# !/usr/bin/env python
import logging, time
from kafka import KafkaProducer
import numpy as np

class Producer(object):
    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        while True:
            try:
                msg = input("Enter a message for the consumer: ")
                ride_info = self.get_nparray_ride_info_from_string(msg)
                producer.send('my-topic', ride_info.tobytes())
                print("Producer sent messages!")
            except Exception as e:
                print(e)
                print("Exception occurred, closing producer...")
                producer.close()

    def get_nparray_ride_info_from_string(self, ride_info_string):
        ride_info = ride_info_string.split(",")
        ride_info = [data.strip() for data in ride_info]
        ride_info = [float(data) for data in ride_info]
        return np.asarray(ride_info)

def main():
    producer = Producer()
    producer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
