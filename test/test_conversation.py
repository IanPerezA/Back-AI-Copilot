# tests/test_conversation.py

from app.services.conversation_service import ConversationService
from app.models.schemas import ConversationState


def test_detect_intent():
    cs = ConversationService()

    assert cs.detect_intent("/nota comprar") == "nota"
    assert cs.detect_intent("/recordatorio mañana") == "recordatorio"
    assert cs.detect_intent("/busqueda clima") == "busqueda"
    assert cs.detect_intent("hola como estas") == "default"


def test_extract_user_context():
    cs = ConversationService()
    state = ConversationState()

    cs.extract_user_context("Me llamo Ian", state)
    cs.extract_user_context("vivo en Monterrey", state)

    assert state.user_context["nombre"] == "Ian"
    assert state.user_context["ciudad"] == "Monterrey"


def test_add_and_truncate_history():
    cs = ConversationService()
    state = ConversationState(max_turns=3)

    cs.add_user_turn(state, "1")
    cs.add_user_turn(state, "2")
    cs.add_user_turn(state, "3")
    cs.add_user_turn(state, "4")

    assert len(state.history) == 3
    assert state.history[0].content == "2"
