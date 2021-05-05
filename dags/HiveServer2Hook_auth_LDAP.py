# https://dydwnsekd.tistory.com/51

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.apache.hive.hooks.hive import *
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args= {
    'start_date': days_ago(1),
    'retries': 0,
    'catchup': False,
    'retry_delaty': timedelta(minutes=5),
}

def simple_query():
    hql = 'SELECT * FROM airflow LIMIT 10'
    hm = HiveServer2Hook(hiveserver2_conn_id='HiveServer2_test')
    #result = hm.get_records(hql, "[db_name]")
    result = hm.get_records(hql, "test_airflow")

    print(result)

    for i in result:
        print(i)
    
dag = DAG(
        'hivehook_test', 
        default_args=default_args, 
        schedule_interval="@once",
    )

t1 = PythonOperator(
    task_id='HiveServer2Hook_test',
    python_callable=simple_query,
    dag=dag,
)

