from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id = 'execution_date_hourly',
    start_date = datetime(2021,9,25),
    catchup=True,
    tags=['example'],
    schedule_interval = '@hourly',
)

print_execution_date = BashOperator(
    task_id = 'execution_date',
    bash_command="echo {{execution_date}}",
    dag = dag
)

print_execution_date