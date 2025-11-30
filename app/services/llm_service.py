import os
import time
from typing import Any, Dict, List
from app.models.schemas import LLMResponse , AgentMessage
import httpx

class LLMProvider:
    provider_name:str
    default_model:str
    
    async def generate(self,messages:List[AgentMessage],params:Dict[str,Any]) -> LLMResponse: 
        raise NotImplementedError("Este método debe ser implementado por subclases")
    
class GroqProvider(LLMProvider):
    provider_name = "Groq"

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate(self, messages: List[AgentMessage], params: Dict[str, Any]) -> LLMResponse:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no está configurada en las variables de entorno")

        payload_messages = [{"role": m.role, "content": m.content} for m in messages]

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "max_tokens": params.get("max_tokens", 256),
            "temperature": params.get("temperature", 0.4),
            "top_p": params.get("top_p", 0.9)
        }

        retries = 3
        delay = 1

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    start = time.time()
                    res = await client.post(
                        self.url,
                        json=payload,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        }
                    )
                    elapsed = (time.time() - start) * 1000

                    if res.status_code == 200:
                        data = res.json()
                        choice = data["choices"][0]["message"]["content"]
                        return LLMResponse(
                            response_content=choice,
                            provider=self.provider_name,
                            model=self.model_name,
                            tokens_in=data.get("usage", {}).get("prompt_tokens"),
                            tokens_out=data.get("usage", {}).get("completion_tokens"),
                            latency_ms=elapsed,
                            fallback=False,
                            log=data
                        )
                    else:
                        raise Exception(res.text)

            except Exception as e:
                if attempt == retries - 1:
                    print(">> ERROR: Groq veamos que le dolio .😂😂😂", e)
                    return LLMResponse(
                        response_content="Estoy teniendo problemas técnicos con el proveedor Groq.⚠️⚠️⚠️⚠️",
                        provider=self.provider_name,
                        model=self.model_name,
                        fallback=True
                    )
                await self._sleep(delay)
                delay *= 2
                

        return LLMResponse(
            response_content="Estoy teniendo problemas técnicos con Groq.❌❌❌",
            provider=self.provider_name,
            model=self.model_name,
            fallback=True
        )

    async def _sleep(self, seconds):
        import asyncio
        await asyncio.sleep(seconds)


class HFProvider(LLMProvider):

    provider_name = "huggingface"

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = os.getenv("HF_API_KEY")
        self.url = "https://router.huggingface.co/v1/chat/completions"

    async def generate(self, messages: List[AgentMessage], params: Dict[str, Any]) -> LLMResponse:
        if not self.api_key:
            raise ValueError("HF_API_KEY no configurada en el entorno")

        payload_messages = [{"role": m.role, "content": m.content} for m in messages]

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "max_tokens": params.get("max_tokens", 256),
            "temperature": params.get("temperature", 0.4),
            "top_p": params.get("top_p", 0.9)
        }

        retries = 3
        delay = 1

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    start = time.time()
                    res = await client.post(
                        self.url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json=payload
                    )
                    elapsed = (time.time() - start) * 1000

                    if res.status_code == 200:
                        data = res.json()
                        content = data["choices"][0]["message"]["content"]
                        usage = data.get("usage", {})
                        return LLMResponse(
                            response_content=content,
                            provider=self.provider_name,
                            model=self.model_name,
                            tokens_in=usage.get("prompt_tokens"),
                            tokens_out=usage.get("completion_tokens"),
                            latency_ms=elapsed,
                            fallback=False,
                            log=data
                        )
                    else:
                        raise Exception(res.text)

            except Exception as e:
                if attempt == retries - 1:
                    print(">> ERROR: HuggingFace veamos que le dolio .👾👾👾", e)
                    return LLMResponse(
                        response_content="Teniendo problemas técnicos con HuggingFace.",
                        provider=self.provider_name,
                        model=self.model_name,
                        fallback=True
                    )
                await self._sleep(delay)
                delay *= 2

        return LLMResponse(
            response_content="Teniendo problemas técnicos con HuggingFace.",
            provider=self.provider_name,
            model=self.model_name,
            fallback=True
        )


    async def _sleep(self, seconds):
        import asyncio
        await asyncio.sleep(seconds)


# este ultimo metodo es para orquestar a los proovedores
def get_provider(name:str,model:str) -> LLMProvider:
    if name.lower() == "groq":
        return GroqProvider(model_name=model)
    elif name.lower() == "huggingface":
        return HFProvider(model_name=model)
    else:
        raise ValueError(f"Proveedor no soportado: {name}")

        