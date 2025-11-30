import requests
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

print(">> DEBUG: buscando .env:", ENV_PATH)

load_dotenv(ENV_PATH)

api_key = os.getenv("HF_API_KEY")
print(">> DEBUG: HF_API_KEY cargada:", bool(api_key))

if not api_key:
    raise EnvironmentError("HF_API_KEY no está definida en .env")

url = "https://huggingface.co/api/models?full=true"   

headers = {
    "Authorization": f"Bearer {api_key}"
}

print(">> Enviando solicitud a HuggingFace...")
res = requests.get(url, headers=headers)

print(">> STATUS:", res.status_code)

if res.status_code != 200:
    print(">> ERROR:", res.text)
    exit()

models = res.json()

print(f">> Total modelos accesibles: {len(models)}")


print(">> Modelos útiles para inferencia:\n")

for m in models:
    if "pipeline_tag" in m and m["pipeline_tag"] in ["text-generation", "text2text-generation"]:
        print(f"- {m['modelId']}  ({m['pipeline_tag']})")
