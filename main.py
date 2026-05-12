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

SYSTEM_PROMPT = """Tu es l'assistant de {nom}.
{description}
- Réponds dans la même langue que le client (Darija, Français, Anglais)
- Pour le Darija : utilise le latin marocain (wach, mzyan, bghit...)
- Maximum 3 phrases courtes
- Si tu ne sais pas : "Contactez-nous : {whatsapp}"
{faq}"""

CONFIG = {
    CONFIG = {
    "nom": "Ahle Addiafa Traiteur",
    "description": "Traiteur, Pâtissier et Chocolatier à Rabat. Créateur d'émotions gourmandes depuis 1996. Spécialiste des mariages et événements.",
    "whatsapp": "+212 5 37 72 01 02",
    "faq": """
    - Adresse : 7 Rue Stockholm, Océan, Rabat
    - Tel : 05 37 72 01 02
    - Services : mariages, fiançailles, Drib Sdak, anniversaires
    - Spécialités : pâtisserie marocaine, chocolats, buffets, couscous
    - Devis gratuit sur demande
    """
}
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
model="llama-3.3-70b-versatile",        messages=messages,
        max_tokens=300
    )
    return {"reply": response.choices[0].message.content}

@app.get("/")
def test():
    return {"status": "chatbot en ligne"}
