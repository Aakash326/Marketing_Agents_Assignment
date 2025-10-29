import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# HF_TOKEN = os.environ.get("HF_TOKEN")
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-4o-mini"

# HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
# Use absolute path for vector store to work from any directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_FAISS_PATH = str(PROJECT_ROOT / "vectorstore" / "db_faiss")
DATA_PATH = "data/"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50