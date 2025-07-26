import os
import re
import chromadb
from pypdf import PdfReader
from typing import List
import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv

load_dotenv()

# Embedding function
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model = "models/embedding-001"
        title = "customer query"
        return genai.embed_content(
            model=model,
            content=input,
            task_type="retrieval_document",
            title=title
        )["embedding"]

# Charger PDF
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Split texte
def split_text(text):
    return [i for i in re.split('\n\n', text) if i.strip()]

# Créer ChromaDB
def create_chroma_db(documents: List[str], path: str, name: str):
    chroma_client = chromadb.PersistentClient(path=path)
    db = chroma_client.get_or_create_collection(
        name=name,
        embedding_function=GeminiEmbeddingFunction()
    )
    for i, d in enumerate(documents):
        db.add(documents=[d], ids=[str(i)])
    return db

# Charger Chroma existant
def load_chroma_collection(path: str, name: str):
    chroma_client = chromadb.PersistentClient(path=path)
    return chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())

# Trouver passage pertinent
def get_relevant_passage(query: str, db, n_results: int):
    results = db.query(query_texts=[query], n_results=n_results)
    return [doc[0] for doc in results['documents']]

# Construire prompt
def make_rag_prompt(query: str, relevant_passage: str):
    escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = f"""Vous êtes un bot utile et informatif qui répond aux questions en utilisant le texte de référence inclus ci-dessous.
Répondez de manière claire et amicale.

QUESTION: '{query}'
PASSAGE: '{escaped_passage}'
ANSWER:"""
    return prompt

# Générer réponse
def generate_answer(prompt: str):
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    result = model.generate_content(prompt)
    return result.text
