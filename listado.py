import requests
import os
from dotenv import load_dotenv
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent

ENV_PATH = CURRENT_DIR / ".env"


print(">> DEBUG: Buscando .env en:", ENV_PATH)

if not ENV_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo .env en: {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("GROQ_API_KEY")
print(">> DEBUG: GROQ_API_KEY cargada:", bool(api_key))

if not api_key:
    raise EnvironmentError("GROQ_API_KEY no está definida en el .env.")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print(">> Enviando solicitud a Groq...")
response = requests.get(url, headers=headers)

print(">> STATUS:", response.status_code)

if response.status_code != 200:
    print(">> ERROR:", response.text)
else:
    print(">> Modelos disponibles:")
    print(response.json())

