from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.controllers.chat_controller import ChatController

router = APIRouter()
controller = ChatController()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    return await controller.handle_chat(request)
