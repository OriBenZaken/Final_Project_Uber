# !/usr/bin/env python
import logging
import time
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
import numpy as np

WAIT_TIME_UNTIL_RETRY_CONNECTION = 10 # In seconds

##############################################
########### Kafka Producer Class #############
##############################################

class Producer(object):
    def run(self):
        """
        runs the producer code
        producer sends new queries to kafka queue
        """
        while True:
            try:
                print("Kafka Producer: Trying to establish connection to kafka server...")
                producer = KafkaProducer(bootstrap_servers='localhost:9092')
                print("Kafka Producer: Succeeded to establishe connection to kafka server.")
                while True:
                    try:
                        msg = input("Enter a new ride info: \n"
                                    "<longitude, base, weekday, day, month, year, hour, isWeekend, isHoliday>")
                        #ride_info = self.get_nparray_ride_info_from_string(msg)
                        producer.send('my-topic-2', msg.encode())
                        print("Producer sent messages!")
                    except Exception as e:
                        print(e)
                        print("Exception occurred, closing producer...")
                        producer.close()
                        break
            except NoBrokersAvailable:
                time.sleep(WAIT_TIME_UNTIL_RETRY_CONNECTION)




def main():
    """
    main function
    runs the program
    """
    producer = Producer()
    producer.run()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.CRITICAL
    )
    main()
