#!/bin/bash

echo Building hello-kafka (Kafka producer) image...
sudo docker build -t hello-kafka -f Dockerfile_hello_kafka .

echo Building i9e (Insightedge + Kafka consumer) image...
sudo docker build -t i9e -f Dockerfile-i9e .
