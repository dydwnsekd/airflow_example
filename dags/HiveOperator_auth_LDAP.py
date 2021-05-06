# https://dydwnsekd.tistory.com/52

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.apache.hive.hooks.hive import *
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.utils.dates import days_ago

default_args= {
    'start_date': days_ago(1),
    'retries': 0,
    'catchup': False,
    'retry_delay': timedelta(minutes=0),
}

dag = DAG(
    'HiveOperator_test',
    default_args=default_args,
    schedule_interval="@once"
)

hql='''
    CREATE TABLE if not exists test_airflow.airflow(
            id STRING,
            name STRING
        );
    '''

t1 = HiveOperator(
    task_id='HiveOperator_test',
    hql=hql,
    hive_cli_conn_id='hive_cli_connect',
    run_as_owner=True,
    dag=dag,
)