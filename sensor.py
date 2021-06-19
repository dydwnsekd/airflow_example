from airflow import DAG
from datetime import datetime, timedelta
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args= {
    'start_date': days_ago(1),
    'retries': 0,
    'catchup': False,
    'retry_delay': timedelta(minutes=5),
}
    
dag = DAG(
        'sensor_test', 
        default_args=default_args, 
        schedule_interval="@once",
)

t1 = FileSensor(
    task_id='sensor_a',
    fs_conn_id='file_sensor',
    filepath='a.txt',
    dag=dag,
)

t2 = BashOperator(
    task_id='cat_a',
    bash_command='cat /opt/airflow/sensor/a.txt',
    dag=dag,
)

t1 >> t2