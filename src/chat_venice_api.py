from typing import Dict, Any
from langchain_openai import ChatOpenAI

class ChatVeniceAPI(ChatOpenAI):
    def __init__(self, model: str, api_key: str, base_url: str, **kwargs):
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )

    @property
    def _default_params(self) -> Dict[str, Any]:
        params = super()._default_params
        if 'n' in params:
            del params['n']
        return params
