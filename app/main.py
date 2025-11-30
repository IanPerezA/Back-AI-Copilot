from fastapi import FastAPI
from app.routers.chat_router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pathlib
import os

dotenv_path = pathlib.Path(__file__).parent.parent / ".env"
print(">> DEBUG DOTENV PATH:", dotenv_path, dotenv_path.exists())

load_dotenv(dotenv_path)

print(">> DEBUG API KEY AFTER LOAD:", os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title ="AI Copilot API",
    version ="1.0.0",
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://front-ai-copilot.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bienvenido a la  AI Copilot API"} 