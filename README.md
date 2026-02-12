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

### 4. 4. Execution

