from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

PROMPT = "Tu es l'assistant de Ahle Addiafa Traiteur a Rabat. Reponds en Darija, Francais ou Anglais selon le client. Max 3 phrases. WhatsApp: +212537720102"

class Msg(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(msg: Msg):
    messages = [{"role": "system", "content": PROMPT}]
    for h in msg.history:
        messages.append(h)
    messages.append({"role": "user", "content": msg.message})
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, max_tokens=300)
    return {"reply": response.choices[0].message.content}

@app.get("/")
def home():
    return FileResponse("test.html")

@app.get("/status")
def status():
    return {"status": "ok"}