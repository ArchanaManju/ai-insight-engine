About the project 

ingest.py 
1. Data Ingestion (The "Extract")
Took raw marketing data and performed "Data Sanitization."
loaded a file;handled missing values (dropna) and ensured data types were consistent (astype(str)).

2. Embedding Generation (The "Transform")
used a PyTorch-based model (all-MiniLM-L6-v2) to turn human language into math.[Vector]
 Instead of simple keyword matching (like Ctrl+F), created Vector Embeddings. This allows the engine to understand that "battery life" is related to "power consumption" even if the words are different.

3. Vector Storage (The "Load")
used ChromaDB as a "Persistent Vector Database."
Didnot just store it in RAM; saved it to disk in chroma_db/.System doesn't have to re-process the data every time it starts—it's "Production Ready."

query.ps
4. Semantic Retrieval (The "Search")
When asked a question, the system performed a Cosine Similarity Search.
It looked for the closest "mathematical neighbors" to your question. That’s why you got results about "enjoying daily use" when you asked about "positive aspects."