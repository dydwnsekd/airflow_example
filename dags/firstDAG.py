from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'start_date': days_ago(1),
}

dag = DAG(
    'firstDAG_test',
    default_args=default_args,
    schedule_interval="@once",
)

def Hello_airflow():
    print("Hello airflow")

t1 = BashOperator(
    task_id='bash',
    bash_command='echo "Hello airflow"',
    dag=dag,
)

t2 = PythonOperator(
    task_id='python',
    python_callable=Hello_airflow,
    dag=dag,
)

t1 >> t2