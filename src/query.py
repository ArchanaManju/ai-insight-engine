import chromadb
import requests
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv, find_dotenv

# 1. Load Environment
load_dotenv(find_dotenv())

def get_llm_response(question, context): 
    prompt =f"""
    You are an Marketing Analyst. Use the following reviews to answer the question.
    If the answer isn't in the context, say you don't know
    Context: {context}
    Question: {question}
    
    Answer:"""

    response = requests.post("http://localhost:11434/api/generate", 
                             json={"model": "llama3", "prompt": prompt, "stream": False})
    if response.status_code == 200: 
        return response.json()['response']
    else:
        print(f"Error: LLM API returned status code {response.status_code}")
        return "Sorry, I'm having trouble generating a response right now."

def query_insights(user_question):
    chroma_path = os.getenv("CHROMA_PATH")
   # Setup ChromaDB client and collection
    client = chromadb.PersistentClient(chroma_path)
    collection = client.get_collection("marketing_insights")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    #1. Retrieval - Get top 2 relevant reviews from ChromaDB
    query_embedding = model.encode(user_question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    #2. Genration# Combine retrieved reviews into a single context string
    context_str = "\n".join(results['documents'][0])
    print(f"\n--- Generating Report for: {user_question} ---")

    report = get_llm_response(user_question, context_str)
    print(f"\nAI ANALYST REPORT:\n{report}")


if __name__ == "__main__":
    user_question = "What are the most positive aspects mentioned in the reviews?"
    query_insights(user_question)