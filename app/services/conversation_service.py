import re
from typing import Optional

from app.models.schemas import ConversationState, ConversationTurn

class ConversationService:
    
    def __init__(self):
        self.sessions = {}
    
    def get_state(self, session_id: Optional[str])-> ConversationState:
        
        if not session_id:
            session_id = "default"
            
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationState()
        
        return self.sessions[session_id]
    
    def detect_intent(self, user_input: str) -> str:
        cleaned = user_input.strip().lower()

        if cleaned.startswith("/nota"):
            return "nota"

        if cleaned.startswith("/recordatorio"):
            return "recordatorio"

        if cleaned.startswith("/busqueda") or cleaned.startswith("/busqueda"):
            return "busqueda"

        return "default"
    
    
    def add_user_turn(self, state: ConversationState, content: str):
        self.extract_user_context(content, state)
        state.history.append(
            ConversationTurn(role="user", content=content)
        )
        self._truncate(state)

    def add_assistant_turn(self, state: ConversationState, content: str):
        state.history.append(
            ConversationTurn(role="assistant", content=content)
        )
        self._truncate(state)
        
    def _truncate(self, state: ConversationState):
        """Borra mensajes si exceden el máximo."""
        max_turns = state.max_turns
        if len(state.history) > max_turns:
            excess = len(state.history) - max_turns
            state.history = state.history[excess:]
    
    def extract_user_context(self, user_input: str, state: ConversationState):


        cleaned = user_input.strip().lower()

        name_match = re.search(r"(me llamo|mi nombre es)\s+([a-záéíóúñ]+)", cleaned)
        if name_match:
            name = name_match.group(2).strip().capitalize()
            state.user_context["nombre"] = name


        city_match = re.search(r"(vivo en|estoy en|soy de)\s+([a-záéíóúñ\s]+)", cleaned)
        if city_match:
            city = city_match.group(2).strip().capitalize()
            state.user_context["ciudad"] = city


        job_match = re.search(r"(soy|trabajo como)\s+([a-záéíóúñ\s]+)", cleaned)
        if job_match:
            job = job_match.group(2).strip().capitalize()
            state.user_context["ocupacion"] = job


