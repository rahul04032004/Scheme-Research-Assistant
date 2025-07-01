import requests
from bs4 import BeautifulSoup
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_url(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return str(e)

def embed_and_index(texts):
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings

def save_index(index, file_path='faiss_store_gemini.pkl'):
    with open(file_path, 'wb') as f:
        pickle.dump(index, f)

def load_index(file_path='faiss_store_gemini.pkl'):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None
