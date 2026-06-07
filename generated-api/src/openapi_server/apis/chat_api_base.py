# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import List
from openapi_server.models.chat_history_item import ChatHistoryItem
from openapi_server.models.chat_request import ChatRequest
from openapi_server.models.chat_response import ChatResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseChatApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseChatApi.subclasses = BaseChatApi.subclasses + (cls,)
    async def chat(
        self,
        chat_request: ChatRequest,
    ) -> ChatResponse:
        """Ask a financial question using the RAG system."""
        ...


    async def get_chat_history(
        self,
    ) -> List[ChatHistoryItem]:
        """Retrieve previous chat interactions for the authenticated user."""
        ...
