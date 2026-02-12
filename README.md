## 🚀 How to Run the AMD AI Insight Engine

### 1. Prerequisites
* **Python 3.9+**
* **Ollama** (Download from [ollama.com](https://ollama.com))
* **Llama 3 Model**: Run `ollama run llama3` in your terminal.

### 2. Installation
```bash
# Clone the repository
git clone "https://github.com/ArchanaManju/ai-insight-engine"
cd amd-ai-insight-engine

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

### 3. Data Setup
# Create a .env file in the root directory: 
# Place your marketing CSV in the data/ folder
DATA_PATH=./data/marketing_data.csv
CHROMA_PATH=./chroma_db

### 4. Execution
# Step 1: Ingest and Vectorize the data
python src/ingest.py

# Step 2: Query the engine for insights
python src/query.py


🏗️ System ArchitectureThis project implements a Retrieval-Augmented Generation (RAG) architecture, decoupled into two primary stages to ensure high-performance data handling and reliable AI inference.


1. Ingestion Phase (ingest.py)The ingestion pipeline handles the ETL (Extract, Transform, Load) process for unstructured marketing data:
    Data Extraction: Loads raw customer feedback from marketing_data.csv using Pandas.
    Preprocessing: Performs data sanitization, handling missing values and ensuring text normalization for higher embedding quality.
    Vectorization: Utilizes a PyTorch-based Transformer model (all-MiniLM-L6-v2) to convert text into high-dimensional vector embeddings.
    Persistence: Stores vectors and associated metadata in ChromaDB, an AI-native persistent vector database, preventing the need for costly re-computation.
2. Inference Phase (query.py)The query pipeline executes the retrieval and generation logic in real-time:
    SemanticSearch: The user's natural language question is embedded using the same PyTorch model and compared against the vector store using Cosine Similarity.
    ContextAugmentation: The top $N$ most relevant insights are retrieved and injected into a structured prompt.
    LocalLLMGeneration: A localized instance of Llama 3 (via Ollama) synthesizes the retrieved context into a coherent, professional marketing report.