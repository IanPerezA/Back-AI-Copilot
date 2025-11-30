from typing import List
from app.models.schemas import AgentMessage, AgentBuildResult, ConversationState
from .base_agent import AgentStrategy


class DefaultChatAgent(AgentStrategy):

    def system_prompt(self) -> str:
        return (
            "Eres un asistente conversacional útil, claro y amable. "
            "Responde con precisión y naturalidad."
        )

    def select_provider(self) -> str:
        return "groq"

    def select_model(self) -> str:
        return "llama-3.1-8b-instant"
