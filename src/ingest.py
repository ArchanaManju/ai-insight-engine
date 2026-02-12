import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
import os
from dotenv import load_dotenv, find_dotenv


    
# This will find the .env file regardless of where you run the script from
load_dotenv(find_dotenv())

# Debugging tip: Add this line to see if it's actually working
print(f"DEBUG: DATA_PATH is {os.getenv('DATA_PATH')}")



# This will find the .env file regardless of where you run the script from
load_dotenv(find_dotenv())

# Debugging tip: Add this line to see if it's actually working
print(f"DEBUG: CHROMA_PATH is {os.getenv('CHROMA_PATH')}")

def run_ingestion():
    data_path = os.getenv("DATA_PATH")
    chroma_path = os.getenv("CHROMA_PATH")

    print("Step 1: Starting ingestion process...")

    # 1. Load and clean
    df = pd.read_csv(data_path)
    print(f"DEBUG: Original rows: {len(df)}")
    
    # Clean specifically the review text column
    df = df.dropna(subset=['reviews.text'])
    print(f"DEBUG: CSV shape after dropna: {df.shape}")

    if(len(df) > 1000):
        df = df.head(1000) # Limit to 1000 rows for testing
        print("DEBUG: Limited to 1000 rows for testing.")

    if df.empty:
        print("Error: The CSV is empty after cleaning. Check your data!")
        return
    
    # Convert to List of Strings
    documents = df['reviews.text'].astype(str).tolist()
    ids = [str(i) for i in range(len(documents))]
    #Add metadata so we know where the data came from 
    metadatas = [{"source":'marketing_data.csv', 'row':i} for i in range(len(documents))]
    
    print(f"Step 2: Connecting to ChromaDB at {chroma_path}...")
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection("marketing_insights")

    print("Step 3: Encoding with PyTorch (SentenceTransformer)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model .encode(documents).tolist()

    # Safety check: ensure embeddings aren't empty
    if not embeddings:
        print("Error: No embeddings were generated. Check your model and data!")
        return
    
    print("Step 4: Adding vectors to ChromaDB...")
    
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully ingested {len(documents)} documents into ChromaDB ")

if __name__ == "__main__":
    run_ingestion()