from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models.variable import Variable

a_user = Variable.get("a_user")
a_password = Variable.get("a_password")

default_args = {
    'start_date': days_ago(1),
}

dag = DAG(
    'Varialbes_dag',
    default_args=default_args,
    schedule_interval="@once",
)

t1 = BashOperator(
    task_id='variable_get',
    bash_command='echo {a_user} / {a_password}'.format(a_user=a_user, a_password=a_password),
    dag=dag,
)

t2 = BashOperator(
    task_id='variable_jinja',
    bash_command='echo {{ var.value.a_user }} / {{ var.value.a_password }}',
    dag=dag,
)

t1 >> t2