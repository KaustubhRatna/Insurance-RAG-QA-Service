# embedder/embed.py

from sentence_transformers import SentenceTransformer
from typing import List
from config import settings
import torch

# 1) Load your local model
_model = SentenceTransformer(settings.EMBEDDING_MODEL_PATH, device='cuda' if torch.cuda.is_available() else 'cpu')

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed a list of texts (e.g. document chunks).
    """
    embeddings = _model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.tolist()

def embed_query(text: str) -> List[float]:
    """
    Embed a single query string.
    """
    vec = _model.encode([text], convert_to_numpy=True, show_progress_bar=False)
    return vec[0].tolist()

def get_embedding_dimension() -> int:
    """
    Returns the model’s embedding dimension.
    """
    return _model.get_sentence_embedding_dimension()

def get_max_input_tokens() -> int:
    """
    Returns the maximum number of tokens that the model can handle as input.
    """
    return _model.tokenizer.model_max_length
