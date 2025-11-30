from app.models.schemas import AgentMessage, AgentBuildResult,ConversationState
from .base_agent import AgentStrategy

class NotesAgent(AgentStrategy):
    def system_prompt(self):
        return(
            "Eres un agente especializado en tomar notas, por lo que debes sintetizar informacion y capturar ideas principales."
            "Convierte el texto proporcionado en notas claras y concisas. Prestando atencion a fechas, horas, nombres y detalles relevantes."
        )
    def select_provider(self) -> str:
        return "huggingface"
    
    def select_model(self) -> str:
        return "meta-llama/Meta-Llama-3-8B-Instruct"

    
    def llm_params(self):
        return {
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 200
        }
    