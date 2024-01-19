#!/bin/bash


pip install -r requirements.txt
# Get airflow environment variables
source .env.dev

# Initialize airflow database
airflow db init

# Create airflow user
airflow users create \
    --username enri \
    --firstname enrique \
    --lastname jr \
    --role Admin \
    --email ejimenez@myfieldaudits.com

airflow webserver --port 8080

