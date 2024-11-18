import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ollama_address = os.getenv("OLLAMA_ADDRESS")
ollama_port = os.getenv("OLLAMA_PORT")


def generate(query, docs, sources, distance, model, temperature):
    prompt = (f"{query} - Rispondi alla domanda in italiano basandoti ESCLUSIVAMENTE sui seguenti documenti relativi ad appunti universitari di ingegneria informatica."
              f"\nLa risposta deve essere completa, accurata e fornire dettagli rilevanti in relazione al contesto disponibile."
              f"\nNota bene: se nel contesto seguente ci sono degli esempi, non considerarli per fornire la spiegazione."
              f"\nIl contesto è:\n{docs}")

    url = f"http://{ollama_address}:{ollama_port}/api/generate"

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_thread": 8,
            "temperature": temperature
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json().get('response', 'Error in generating response')

    return {"response": response, "sources": sources, "distance": distance}
