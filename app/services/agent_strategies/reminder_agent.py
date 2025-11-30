from typing import Dict
from app.models.schemas import AgentMessage, AgentBuildResult,ConversationState
from .base_agent import AgentStrategy
from datetime import datetime, timezone

class ReminderAgent(AgentStrategy):
    
    def get_now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def system_prompt(self):
        now = self.get_now_iso()
        return f"""
            Eres un agente especializado en crear recordatorios.

            Contexto de tiempo:
            La fecha y hora actual del sistema es: {now}

            Tu tarea:
            - Interpretar tiempos relativos como "en 15 minutos", "mañana a las 3pm",
            "dentro de 2 horas", "el próximo viernes", etc.
            - Convertirlos SIEMPRE a una fecha absoluta en formato ISO 8601.
            - Si el usuario no indicó fecha ni tiempo, pídele aclaración.
            - NO es necesario mencionarle al usuario que estas realizando esta conversión.
            - Solo muestrale a usuario la fecha y hora del recordatorio 
            - fecha en formato dd/mm/aaaa y hora en formato 24 horas HH:MM
            - Devuelve SIEMPRE un JSON con la estructura:

            {{
            "titulo": "<mensaje corto>",
            "descripcion": "<detalle opcional>",
            "fecha_ejecucion": "<fecha absoluta en ISO 8601>"
            }}

            puedes agrergar detalles adicionales en la descripción si es necesario.
            """
        
    def select_provider(self) -> str:
        return "groq"
    
    def select_model(self) -> str:
        return "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    def llm_params(self) -> Dict:
        return {"temperature": 0.3, "max_tokens": 255}
      