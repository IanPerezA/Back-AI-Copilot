import re
from typing import Dict
from app.models.schemas import ConversationState, AgentMessage


class PromptingService:


    def clean_input(self, text: str) -> str:
        """ Elimina caracteres invisibles y normaliza espacios. """
        if not text:
            return ""

        text = re.sub(r"[\x00-\x1F\x7F]", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def strip_intent_prefix(self, text: str) -> str:
        """ Elimina comandos como /nota, /recordatorio, /busqueda del input. """
        prefixes = ["/nota", "/recordatorio", "/busqueda", "/búsqueda"]

        cleaned = text.strip().lower()
        for p in prefixes:
            if cleaned.startswith(p):
                return cleaned[len(p):].strip()

        return text.strip()

    def prepare_user_input(self, raw_input: str) -> str:
        """
        Pipeline completo para input:
            raw_input → clean_input → strip intent prefix
        """
        cleaned = self.clean_input(raw_input)
        return self.strip_intent_prefix(cleaned)

    def build_context_block(self, state: ConversationState) -> str:
        if not state.user_context:
            return ""

        lines = ["Información previa del usuario:"]
        for key, value in state.user_context.items():
            key_f = key.capitalize()
            value_f = value.strip().capitalize()
            lines.append(f"{key_f}: {value_f}")

        return "\n".join(lines)

    def prepare_messages_for_agent(
        self,
        system_prompt: str,
        conv_state: ConversationState,
        user_input: str
    ) -> list[AgentMessage]:
        """
        Construye el listado base de mensajes:
            - system prompt
            - bloque de contexto (si existe)
            - historial
            - mensaje actual del usuario
        """

        messages = [
            AgentMessage(role="system", content=system_prompt)
        ]

        context_block = self.build_context_block(conv_state)
        if context_block:
            messages.append(
                AgentMessage(role="system", content=context_block)
            )

        for turn in conv_state.history:
            messages.append(
                AgentMessage(role=turn.role, content=turn.content)
            )

        messages.append(
            AgentMessage(role="user", content=user_input)
        )

        return messages
