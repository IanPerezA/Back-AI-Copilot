from fastapi import HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.services.strategy_manager import StrategyManager

conversation_service = ConversationService()
strategy_manager = StrategyManager()


class ChatController:

    async def handle_chat(self, req: ChatRequest) -> ChatResponse:
        try:
            conv_state = conversation_service.get_state(req.session_id)

            intent = conversation_service.detect_intent(req.user_input)

            conversation_service.add_user_turn(conv_state, req.user_input)

            llm_response = await strategy_manager.run(
                intent=intent,
                conv_state=conv_state,
                user_input=req.user_input
            )

            conversation_service.add_assistant_turn(conv_state, llm_response.response_content)
            return ChatResponse(
                response=llm_response.response_content,
                intent=intent,
                session_id=req.session_id,
                provider=llm_response.provider,
                model=llm_response.model,
                tokens_in=llm_response.tokens_in,
                tokens_out=llm_response.tokens_out,
                latency=llm_response.latency_ms,  
                fallback=llm_response.fallback
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
