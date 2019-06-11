#!/bin/bash

sudo nohup ./activate-i9e.sh &
sleep 1m
sudo ./copy-zeppelin-notebook.sh
sudo ./activate-consumer.sh
