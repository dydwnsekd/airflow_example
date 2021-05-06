from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.apache.hive.hooks.hive import *
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args= {
    'start_date': days_ago(1),
    'retries': 0,
    'catchup': False,
    'retry_delay': timedelta(minutes=5),
}

templated_command = """
    echo "ds : {{ ds }}"
    echo "ds_nodash : {{ ds_nodash }}"
    echo "prev_ds : {{ prev_ds }}"
    echo "prev_ds_nodash : {{ prev_ds_nodash }}"
    echo "next_ds : {{ next_ds }}"
    echo "next_ds_nodash : {{ next_ds_nodash }}"
    echo "yesterday_ds : {{ yesterday_ds }}"
    echo "yesterday_ds_nodash : {{ yesterday_ds_nodash }}"
    echo "tomorrow_ds : {{ tomorrow_ds }}"
    echo "tomorrow_ds_nodash : {{ tomorrow_ds_nodash }}"
    echo "ts : {{ ts }}"
    echo "ts_nodash : {{ ts_nodash }}"
    echo "ts_nodash_with_tz : {{ ts_nodash_with_tz }}"
    echo "macros.ds_add(ds, 2) : {{ macros.ds_add(ds, 2) }}"
    echo "macros.ds_add(ds, -2) : {{ macros.ds_add(ds, -2) }}"
    echo "macros.ds_format(ds, '%Y-%m-%d', '%Y__%m__%d'): {{ macros.ds_format(ds, '%Y-%m-%d', '%Y__%m__%d') }}"
    echo "macros.datetime.now() : {{ macros.datetime.strftime(macros.datetime.now(), '%Y%m%d%H') }}"
"""

def templated_test(d1):
    print("{{ ds }}")
    print("ds test:", d1)
    
dag = DAG(
        'templated_test', 
        default_args=default_args, 
        schedule_interval="@daily",
    )

t1 = BashOperator(
    task_id='bash_templated',
    bash_command=templated_command,
    dag=dag,
)

t2 = PythonOperator(
    task_id='python_task',
    python_callable=templated_test,
    op_args=["{{ ds }}"],
    dag=dag,
)

t1 >> t2