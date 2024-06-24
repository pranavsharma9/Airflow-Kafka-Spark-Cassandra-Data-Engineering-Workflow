#!/bin/bash

set -e

# Check if requirements.txt exists and install the requirements
if [ -f "/opt/airflow/requirements.txt" ]; then
    $(command -v pip) install --user -r /opt/airflow/requirements.txt
fi

# Initialize the Airflow database if it doesn't exist
if [ ! -f "/opt/airflow/airflow.db" ]; then
    airflow db init && \
    airflow users create \
        --username admin \
        --password admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@example.com
fi

# Upgrade the Airflow database
$(command -v airflow) db upgrade

# Start the Airflow webserver
exec airflow webserver
