from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests
from kafka import KafkaProducer
import time
import logging

default_args={
    "owner": "pranav",
    "start_date": datetime(2024, 6, 21,10,00),
    'retries': 5,  # Number of retries
    'retry_delay': timedelta(minutes=5),
}

def get_data():
    res=requests.get('https://randomuser.me/api/')
    res=res.json()
    res=res['results'][0]

    return res

def format_data(res):
    data={}
    data['first_name']=res['name']['first']
    data['last_name']=res['name']['last']
    data['gender']=res['gender']
    data['email']=res['email']
    data['address']=str(res['location']['street']['number'])+' '+res['location']['street']['name']+' ,'+res['location']['city']+' ,'+res['location']['state']+' ,'+res['location']['country']
    data['postcode']=res['location']['postcode']
    data['username']=res['login']['username']
    data['dob']=res['dob']['date']
    data['phone']=res['phone']
    data['registered_date']=res['registered']['date']
    data['picture']=res['picture']['medium']

    return data

def stream_data():
    producer=KafkaProducer(bootstrap_servers=['broker:29092'],max_block_ms=5000)
    curr_time=time.time()
    while True:
        if time.time()>curr_time+60:
            break
        try:
            res=get_data()
            res=format_data(res)
            producer.send('user_data',json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f"An error occured: {e}")
            continue


with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
