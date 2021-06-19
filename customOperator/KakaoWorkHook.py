import json
import warnings
from typing import Optional
 
import requests
from requests.auth import HTTPBasicAuth
 
from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook
 
class KakaoWorkhookHook(HttpHook):
    def __init__(
        self,
        http_conn_id=None,
        text='',
        block=False,
        *args,
        **kwargs,
    ):
        super().__init__(http_conn_id=http_conn_id, *args, **kwargs)
        conn = self.get_connection(http_conn_id)
        self.Kakao_URl = conn.host
        self.conversation_id = conn.extra_dejson.get('conversation_id')
        self.text = text
        self.block = block
        self.block_list = []
 
        app_key = conn.extra_dejson.get('app_key')
        self.headers = {
            "Authorization": "Bearer {app_key}".format(app_key=app_key),
            "Content-Type": "application/json"
        }
 
    def makeKakaoMessage(self, text):
        if not self.block:
            return json.dumps({
                "conversation_id": "{conversation_id}".format(conversation_id=self.conversation_id),
                "text": "{text}".format(text=text)
            })
        else:
            return json.dumps({
                "conversation_id": "{conversation_id}".format(conversation_id=self.conversation_id),
                "text": "{text}".format(text=text),
                "blocks": self.block_list
            })
 
    def textBlock(
        self,
        text='text',
    ):
        self.block_list.append({
                "type": "text",
                "text": "{text}".format(text=text),
                "markdown": False
            })
 
    def buttonBlock(
        self,
        text='text',
        style='default',
        action_type='open_system_browser',
        action_name='',
        value="localhost:8080"
    ):
        self.block_list.append({
                "type": "button",
                "text": "{text}".format(text=text),
                "style": "{style}".format(style=style),
                "action_type": "{action_type}".format(action_type=action_type),
                "action_name": "{action_name}".format(action_name=action_name),
                "value": "{value}".format(value=value)
            })
 
    def headerBlock(
        self,
        text='text',
        style='blue'
    ):
        # header을 사용하는 경우 제일 상위에서만 사용 가능
        # kakaoBlocksMaker에서 제일 먼저 add 필요
        self.block_list.append({
            "type": "header",
            "text": "{text}".format(text=text),
            "style": "{style}".format(style=style)
        })
     
    def imagelinkBlock(
        self,
        url="https://airflow.apache.org/docs/apache-airflow/stable/_images/pin_large.png"
    ):
        self.block_list.append({
                "type": "image_link",
                "url": "{url}".format(url=url)
            })
 
    def sendMessage(self, data) -> None:
        r = requests.post(self.Kakao_URl, data=data, headers=self.headers)
 
    def execute(self) -> None:
        data = self.makeKakaoMessage(self.text)
        r = requests.post(self.Kakao_URl, data=data, headers=self.headers)