from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id = 'execution_date_5min',
    start_date = datetime(2021,9,26),
    catchup=True,
    tags=['example'],
    schedule_interval = '*/5 * * * *',
)

print_execution_date = BashOperator(
    task_id = 'execution_date',
    bash_command="echo {{execution_date}}",
    dag = dag
)

print_execution_date