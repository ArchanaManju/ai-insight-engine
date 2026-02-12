## 🚀 How to Run the AI Insight Engine

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

```
---

### 🏗️ System Architecture

This project implements a **Retrieval-Augmented Generation (RAG)** architecture, decoupled into two primary stages to ensure high-performance data handling and reliable AI inference.

1. **Ingestion Phase (`ingest.py`)**: The ingestion pipeline handles the ETL (Extract, Transform, Load) process for unstructured marketing data:
    * **Data Extraction**: Loads raw customer feedback from `marketing_data.csv` using **Pandas**.
    * **Preprocessing**: Performs data sanitization, handling missing values and ensuring text normalization for higher embedding quality.
    * **Vectorization**: Utilizes a **PyTorch-based Transformer model** (`all-MiniLM-L6-v2`) to convert text into high-dimensional vector embeddings.
    * **Persistence**: Stores vectors and associated metadata in **ChromaDB**, an AI-native persistent vector database, preventing the need for costly re-computation.

2. **Inference Phase (`query.py`)**: The query pipeline executes the retrieval and generation logic in real-time:
    * **Semantic Search**: The user's natural language question is embedded using the same PyTorch model and compared against the vector store using **Cosine Similarity**.
    * **Context Augmentation**: The top $N$ most relevant insights are retrieved and injected into a structured prompt.
    * **Local LLM Generation**: A localized instance of **Llama 3** (via Ollama) synthesizes the retrieved context into a coherent, professional marketing report.

---

### 🛠️ Technical Challenges & Solutions

1. **Challenge 1** Empty Embedding Vectors during Ingestion
Issue: The ingestion pipeline initially failed with a ValueError: Expected Embeddings to be non-empty, caused by an empty list being passed to ChromaDB.

* **Root Cause Analysis**:
    **Aggressive Cleaning**: Using a global .dropna() on the entire DataFrame removed rows that had missing metadata (like "User Location"), even if the critical "Review Text" was present.
    **Data Sparsity**: Some rows contained headers but no actual text content, resulting in empty strings that the model could not vectorize.

* **Solution**:
    **Targeted Sanitization**: Refactored the cleaning logic to use df.dropna(subset=['reviews.text']), ensuring rows were only discarded if the primary data source was missing.
    **Pre-Encoding Validation**: Implemented a "Senior-level" defensive check:
    ```bash
        if df.empty:
            print("Error: No data found after cleaning. Aborting to save compute.")
            return
    ```
    **Type Casting**: Added .astype(str) conversion to guarantee the PyTorch model received a consistent input format, preventing silent failures during the embedding process.

1. **Challenge 2** Environment Portability and Path Management
    **Issue**: Scripts failed to locate the .env file or the chroma_db directory when executed from different subdirectories.
* **Solution**:
    **Dynamic Path Discovery**: Integrated python-dotenv with find_dotenv(). This allows the application to dynamically locate the root configuration file regardless of the execution context.
    **Security Best Practice**: Moved sensitive paths and model configurations out of the source code and into environment variables to ensure the project remains production-ready and secure.

---

### 🚀 Future Roadmap & Scaling
* **Hardware Acceleration**: Migrate the PyTorch embedding process to utilize **AMD ROCm** for faster vectorization on Radeon/Instinct hardware.
* **Hybrid Search**: Implement a combination of BM25 (keyword) and Vector (semantic) search to improve retrieval accuracy for technical product names.
* **Asynchronous Ingestion**: Transition the ingestion pipeline to a message-queue architecture (e.g., Celery/RabbitMQ) to handle streaming marketing data in real-time.
