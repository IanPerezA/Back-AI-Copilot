from typing import Dict

from app.models.schemas import (
    ConversationState,
    AgentBuildResult,
    LLMResponse
)

from app.services.llm_service import get_provider

from app.services.agent_strategies.default_chat_agent import DefaultChatAgent
from app.services.agent_strategies.notes_agent import NotesAgent
from app.services.agent_strategies.reminder_agent import ReminderAgent
from app.services.agent_strategies.search_agent import SearchAgent


class StrategyManager:

    def __init__(self):
        self.agent_map = {
            "nota": NotesAgent(),
            "recordatorio": ReminderAgent(),
            "busqueda": SearchAgent(),
            "default": DefaultChatAgent()
        }

    def get_agent(self, intent: str):
        return self.agent_map.get(intent, self.agent_map["default"])

    async def run(
        self,
        intent: str,
        conv_state: ConversationState,
        user_input: str
    ) -> LLMResponse:

        agent = self.get_agent(intent)

        build_result: AgentBuildResult = agent.build_messages(
            conv_state=conv_state,
            user_input=user_input
        )

        provider_name = build_result.provider_name
        model_name = build_result.model_name

        provider = get_provider(provider_name, model_name)

        params = agent.llm_params()

        llm_response = await provider.generate(
            messages=build_result.messages,
            params=params
        )

        return llm_response
