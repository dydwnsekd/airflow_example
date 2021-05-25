from airflow import DAG
from datetime import datetime, timedelta
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
    echo "ds : {{ dag_run.conf.ds|d(execution_date) }}"
    """
    
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

t1