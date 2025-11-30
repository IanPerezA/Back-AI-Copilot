from typing import List, Dict
from app.models.schemas import AgentMessage, AgentBuildResult, ConversationState
from app.services.prompting_service import PromptingService


class AgentStrategy:

    def system_prompt(self) -> str:
        raise NotImplementedError

    def select_provider(self) -> str:
        raise NotImplementedError

    def select_model(self) -> str:
        raise NotImplementedError

    def llm_params(self) -> Dict:
        return {
            "temperature": 0.4,
            "top_p": 0.9,
            "max_tokens": 256
        }


    def build_messages(
        self,
        conv_state: ConversationState,
        user_input: str
    ) -> AgentBuildResult:

        prompt_service = PromptingService()

        clean_input = prompt_service.prepare_user_input(user_input)

        all_messages = prompt_service.prepare_messages_for_agent(
            system_prompt=self.system_prompt(),
            conv_state=conv_state,
            user_input=clean_input
        )


        return AgentBuildResult(
            messages=all_messages,
            provider_name=self.select_provider(),
            model_name=self.select_model()
        )

    
