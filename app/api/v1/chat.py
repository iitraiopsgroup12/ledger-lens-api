from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_chat_service, get_current_user
from app.schemas.auth import UserProfile
from app.schemas.chat import ChatHistoryItem, ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=ChatResponse)
def ask_chat(
    payload: ChatRequest,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    return chat_service.ask(current_user.id, payload.query)


@router.get("/history", response_model=list[ChatHistoryItem])
def get_chat_history(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
) -> list[ChatHistoryItem]:
    return chat_service.get_history(current_user.id)
