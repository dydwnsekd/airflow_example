import json
import warnings
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook

# channel, username, icon_emoji, icon_url, link_names, block
class TeamshookHook(HttpHook):
    def __init__(
        self,
        http_conn_id=None,
        title='',
        title_text='',
        activityTitle='',
        activitySubtitle='',
        message='',
        color='green',
        *args,
        **kwargs,
    ):
        print(http_conn_id)
        super().__init__(http_conn_id=http_conn_id, *args, **kwargs)
        self.conn = self.get_connection(http_conn_id)
        self.teams_url = self.conn.host
        self.title = title
        self.title_text = title_text
        self.activityTitle = activityTitle
        self.activitySubtitle = activitySubtitle
        self.message = message
        self.color = color
        self.color_dict = {'red': 'FF0000', 'green': '00FF00', 'blue': '0000FF'}
        

    def _build_teams_message(self) -> str:
        return {
            "themeColor": self.color_dict[self.color],
            "title": self.title,
            "text": self.title_text,
            "sections" : [
                {
                    "activityTitle": self.activityTitle,
                    "activitySubtitle": self.activitySubtitle,
                    "activityImage":"",
                    "text": self.message
                }
            ]
        }


    def execute(self) -> None:
        teams_message = self._build_teams_message()
        # self.run(
        #     endpoint='',
        #     data=teams_message,
        #     headers = {"cache-control": "no-cache"},
        #     extra_options={'check_response': False},
        # )

        headers = {"cache-control": "no-cache"}
 
        r = requests.post(self.teams_url, json=teams_message, headers=headers)
 
        if int(r.status_code) == 200:
            print("good")