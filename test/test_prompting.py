# tests/test_prompting.py

from app.services.prompting_service import PromptingService
from app.models.schemas import ConversationState


def test_strip_intent_prefix():
    ps = PromptingService()
    
    assert ps.strip_intent_prefix("/nota Comprar leche") == "comprar leche"
    assert ps.strip_intent_prefix("/búsqueda clima hoy") == "clima hoy"


def test_clean_input():
    ps = PromptingService()
    
    dirty = "  Hola   \n  mundo\t "
    assert ps.clean_input(dirty) == "Hola mundo"


def test_build_context_block():
    ps = PromptingService()
    
    state = ConversationState(
        user_context={"nombre": "Ian", "ciudad": "Monterrey"}
    )
    
    block = ps.build_context_block(state)
    
    assert "Nombre: Ian" in block
    assert "Ciudad: Monterrey" in block
