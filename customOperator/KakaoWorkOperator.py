from typing import Any, Dict, Optional
 
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults
from custom_operator.kakaowork.KakaoHook import KakaoWorkhookHook
 
class kakaoWorkOperator(SimpleHttpOperator):
 
    @apply_defaults
    def __init__(
        self,
        *,
        http_conn_id: str,
        text: str,
        block: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.http_conn_id = http_conn_id
        self.text = text
        self.block = block
        self.hook: Optional[KakaoWorkhookHook] = None
 
 
    def execute(self, context: Dict[str, Any]) -> None:
        self.hook = KakaoWorkhookHook(
            self.http_conn_id,
            self.text,
            self.block,
        )
        self.hook.execute()