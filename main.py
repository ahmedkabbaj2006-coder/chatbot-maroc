from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["POST"],
    allow_headers=["Content-Type"])

SYSTEM_PROMPT = "Tu es l'assistant de {nom}. {description} Reponds dans la meme langue que le client (Darija, Francais, Anglais). Pour le Darija utilise le latin marocain. Maximum 3 phrases. Si tu ne sais pas dis: Contactez-nous : {whatsapp}. {faq}"

CONFIG = {
    "nom": "Ahle Addiafa Traiteur",
    "description": "Traiteur Patissier Chocolatier a Rabat depuis 1996.",
    "whatsapp": "+212 5 37 72 01 02",
    "faq": "Adresse: 7 Rue Stockholm Ocean Rabat. Tel: 05 37 72 01 02. Services: mariages fiancailles anniversaires. Devis gratuit sur demande."
}

class Msg(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(msg: Msg):
    system = SYSTEM_PROMPT.format(**CONFIG)
    messages = [{"role": "system", "content": system}]
    for h in msg.history:
        messages.append(h)
    messages.append({"role": "user", "content": msg.message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )
    return {"reply": response.choices[0].message.content}

@app.get("/")
def test():
    return {"status": "chatbot en ligne"}