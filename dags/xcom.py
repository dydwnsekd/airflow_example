from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id = 'xcom_test',
    start_date = datetime(2021,9,23),
    catchup=False,
    tags=['example'],
    schedule_interval='@once'
)

def return_xcom(**context):
    return "xcom!"

def xcom_push_test(**context):
    xcom_value = "xcom_push_value"
    context['task_instance'].xcom_push(key='xcom_push_value', value=xcom_value)

    return "xcom_return_value"

def xcom_pull_test(**context):
    xcom_return = context["task_instance"].xcom_pull(task_ids='return_xcom')
    xcom_push_value = context['ti'].xcom_pull(key='xcom_push_value')
    xcom_push_return_value = context['ti'].xcom_pull(task_ids='xcom_push_task')
    #xcom_push_value = context['task_instance'].xcom_pull(keys='xcom_push_value')

    print("xcom_return : {}".format(xcom_return))
    print("xcom_push_value : {}".format(xcom_push_value))
    print("xcom_push_return_value : {}".format(xcom_push_return_value))


return_xcom = PythonOperator(
    task_id = 'return_xcom',
    python_callable = return_xcom,
    provide_context = True,
    dag = dag
)

xcom_push_task = PythonOperator(
    task_id = 'xcom_push_task',
    python_callable = xcom_push_test,
    provide_context = True,
    dag = dag
)

xcom_pull_task = PythonOperator(
    task_id = 'xcom_pull_task',
    python_callable = xcom_pull_test,
    provide_context = True,
    dag = dag
)

xcom_bash_taskids = BashOperator(
    task_id='bash_xcom_taskids',
    bash_command='echo "{{ task_instance.xcom_pull(task_ids="xcom_push_task") }}"',
    dag=dag
)

xcom_bash_key = BashOperator(
    task_id='bash_xcom_key',
    bash_command='echo "{{ ti.xcom_pull(key="xcom_push_value") }}"',
    dag=dag
)

return_xcom >> xcom_push_task >>xcom_pull_task >> xcom_bash_taskids >> xcom_bash_key