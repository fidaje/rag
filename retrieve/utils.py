import chromadb
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

chroma_address = os.getenv("CHROMA_ADDRESS")
chroma_port = int(os.getenv("CHROMA_PORT"))
chroma_collection_name = os.getenv("CHROMA_DB")
embedding_model = os.getenv("EMBEDDING_MODEL")
ollama_address = os.getenv("OLLAMA_ADDRESS")
ollama_port = os.getenv("OLLAMA_PORT")


def _get_embedding(query):
    url = f"http://{ollama_address}:{ollama_port}/api/embed"

    payload = json.dumps({
        "model": embedding_model,
        "input": query,
        "options": {
            "num_thread": 8
        }
    })

    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response.get("embeddings")


def retrieve(query, top=3):
    chroma_client = chromadb.HttpClient(host=chroma_address, port=chroma_port)
    collection = chroma_client.get_or_create_collection(name=f"{chroma_collection_name}")

    query_embed = _get_embedding([query])

    results = collection.query(query_embeddings=query_embed, n_results=top)

    docs = '\n\n'.join(results['documents'][0])

    distance = results['distances'][0]

    something = [f"{metadata['source']}: {metadata['chunk']}" for metadata in results["metadatas"][0]]
    sources = f"{{{', '.join(something)}}}"

    return docs, sources, distance
