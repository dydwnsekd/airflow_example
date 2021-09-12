from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta
import requests
import logging
import json

dag = DAG(
    dag_id = 'slack_test',
    start_date = days_ago(1),
    max_active_runs = 1,
    catchup = False,
    schedule_interval="@once"
)

send_slack_message = SlackWebhookOperator(
    task_id='send_slack',
    http_conn_id='slack_webhook',
    message='Hello slack',
    dag=dag
)

send_slack_message