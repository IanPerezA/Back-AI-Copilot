from typing import List , Optional,Literal,Dict,Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_input : str=Field(...,description="Input del usuario para el chat")
    session_id : Optional[str]=Field(None,description="ID de la sesión de chat")
    
    
class ChatResponse (BaseModel):
    response : str=Field(...,description="Respuesta generada por el modelo de IA")
    intent: str = Field(...,description="Intent detectado")
    session_id : Optional[str]=Field(None,description="ID de la sesión de chat")
    provider: str=Field(...,description="Proveedor Orquestado")
    model: str=Field(...,description="Modelo orquestado")
    tokens_in : Optional[int]=None
    tokens_out: Optional[int] =None
    latency: Optional[float]=None
    fallback: Optional[bool]=Field(False,description="Indica si la respuesta es de respaldo")
    
    # la siguiente clase es para manejar las respuestas de los proveedores
    
class LLMResponse(BaseModel):
    response_content :str
    provider: str
    model: str
    tokens_in : Optional[int]=None
    tokens_out: Optional[int] =None
    latency_ms: Optional[float]=None
    fallback: bool =False
    log: Optional[Any]=None # este es para capturar la respuesta bruta en caso de querer hacer debug
        
class AgentMessage(BaseModel):
    role: Literal["user","assistant","system"]
    content: str
    
class AgentBuildResult(BaseModel):
    messages: List[AgentMessage]
    provider_name: str
    model_name: str
        
''' aqui abajo vamos a definir clases de control de la conversacion
esto es importante para gestionar turnos, historiales y contextos'''

class ConversationTurn(BaseModel):  
    role: Literal["user","assistant"]
    content: str

class ConversationState(BaseModel):
    history: List[ConversationTurn] = []
    max_turns: int = 20
    user_context: Dict[str,str] ={} 
    
    def add_turn(self, role: Literal["user","assistant"], content: str):
        self.history.append(ConversationTurn(role=role, content=content))
    
    def truncate(self):
        if len(self.history) > self.max_turns:
            excess_turns = len(self.history) - self.max_turns
            self.history = self.history[excess_turns:]
        