# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ──────────────────────────────
    # Authentication / Secrets
    # ──────────────────────────────
    # Bearer token for securing the /hackrx/run endpoint
    AUTH_TOKEN: str

    # Your Google Gemini API key
    GEMINI_API_KEY: str

    # ──────────────────────────────
    # Gemini API Configuration
    # ──────────────────────────────
    GEMINI_API_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/"
    GEMINI_QNA_MODEL: str = "gemini-1.5-flash"

    # ──────────────────────────────
    # Chunking (character‐based)
    # ──────────────────────────────
    CHUNK_SIZE: int = 1800                # max characters per chunk (~500 tokens)
    CHUNK_OVERLAP: int = 100              # overlap between chunks (~50 tokens)

    # ──────────────────────────────
    # Embedding
    # ──────────────────────────────
    # Path to your locally-downloaded HuggingFace model directory
    EMBEDDING_MODEL_PATH: str = r"C:\Projects\SM _ insurance\baseline\rag_insurance\insurance_bert_embed"

    # ──────────────────────────────
    # Vector Store
    # ──────────────────────────────
    VECTOR_DB_PATH: str = r"C:\Projects\SM _ insurance\baseline\rag_insurance\vector_store"

    # ──────────────────────────────
    # RAG / Retrieval
    # ──────────────────────────────
    TOP_K_CHUNKS: int = 5                 # number of chunks to retrieve per query

    # ──────────────────────────────
    # LLM / Prompting
    # ──────────────────────────────
    MAX_LLM_INPUT_TOKENS: int = 30000     # prompt size warning threshold

    # ──────────────────────────────
    # Database Update & Retry
    # ──────────────────────────────
    ALLOW_DB_UPDATE: bool = True          # allow adding new docs to persistent store
    MAX_RETRIES: int = 3                  # number of retry attempts for API errors
    INITIAL_RETRY_DELAY_MS: int = 1000    # base backoff delay in milliseconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate a singleton settings object
settings = Settings()
