#!/bin/bash
export PYSPARK_PYTHON=/usr/bin/python3.6
export PYTHONPATH=/usr/bin/python3.6
cd /usr/local/i9e/gigaspaces-insightedge-enterprise-14.5.0-m7/
./insightedge/spark/bin/spark-submit /usr/local/Consumer.py

