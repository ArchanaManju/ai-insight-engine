### This project follows the RAG (Retrieval-Augmented Generation) pattern, divided into two distinct pipelines:

1. The Ingestion Pipeline (The "Backend")
This is where the data is processed before the user ever asks a question.

Data Source: Raw marketing_data.csv (Customer Reviews).

Processing: Pandas cleans the text and handles missing values.

Embedding Model: A PyTorch-based Transformer (all-MiniLM-L6-v2) converts text into 384-dimensional vectors.

Vector Store: ChromaDB saves these vectors to disk (chroma_db/) for persistent storage.

2. The Retrieval & Generation Pipeline (The "Frontend")
This is what happens when the query.py script runs.

Input: User asks a natural language question.

Vector Search: The question is embedded, and ChromaDB performs a Nearest Neighbor Search to find relevant context.

Augmentation: The retrieved reviews are injected into a specialized Analyst Prompt.

Generation: The Local LLM (Llama 3 via Ollama) synthesizes the final report.