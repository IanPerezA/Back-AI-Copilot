from app.models.schemas import AgentMessage, AgentBuildResult, ConversationState
from .base_agent import AgentStrategy

class SearchAgent(AgentStrategy):

    def system_prompt(self) -> str:
        return (
            "Eres un agente de búsqueda. "
            "Tu tarea es interpretar la consulta del usuario y devolver "
            "información relevante, organizada y verificable."
        )

    def select_provider(self) -> str:
        return "huggingface"

    def select_model(self) -> str:
        return "Qwen/Qwen2.5-7B-Instruct"

    def llm_params(self):
        return {"temperature": 0.1, "max_tokens": 220}

