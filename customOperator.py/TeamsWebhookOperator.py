from typing import Any, Dict, Optional

from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults
from custom_operator.teams.TeamsHook import TeamshookHook

class TeamsWebhookOperator(SimpleHttpOperator):

    @apply_defaults
    def __init__(
        self,
        *,
        http_conn_id: str,
        title: str='',
        title_text: str='',
        activityTitle: str='',
        activitySubtitle: str='',
        message: str = '',
        color: str = 'green',
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.http_conn_id = http_conn_id
        self.title = title
        self.title_text = title_text
        self.activityTitle = activityTitle
        self.activitySubtitle = activitySubtitle
        self.message = message
        self.color = color
        self.hook: Optional[TeamshookHook] = None


    def execute(self, context: Dict[str, Any]) -> None:
        self.hook = TeamshookHook(
            self.http_conn_id,
            self.title,
            self.title_text,
            self.activityTitle,
            self.activitySubtitle,
            self.message,
            self.color,
        )
        self.hook.execute()