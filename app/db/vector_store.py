# # db/vector_store.py

# import faiss
# import numpy as np
# from typing import List, Tuple
# from embedder.embed import get_embedding_dimension

# class SimpleVectorStore:
#     def __init__(self):
#         self.dimension = get_embedding_dimension()
#         self.index = faiss.IndexFlatIP(self.dimension)  # Inner product ≈ cosine if normalized
#         self.text_chunks: List[str] = []

#     def add_documents(self, chunks: List[str], embeddings: List[List[float]]):
#         """
#         Add a batch of (chunk, embedding) pairs to the vector store.
#         """
#         self.text_chunks.extend(chunks)
#         vecs = np.array(embeddings).astype('float32')
#         faiss.normalize_L2(vecs)  # normalize before adding
#         self.index.add(vecs)

#     def search(self, query_vec: List[float], top_k: int = 5) -> List[str]:
#         """
#         Search the vector DB with a query embedding and return top-k matching chunks.
#         """
#         query_np = np.array([query_vec]).astype('float32')
#         faiss.normalize_L2(query_np)
#         distances, indices = self.index.search(query_np, top_k)
#         return [self.text_chunks[i] for i in indices[0] if i < len(self.text_chunks)]

#     def clear(self):
#         """
#         Clears the index and stored chunks.
#         """
#         self.index.reset()
#         self.text_chunks = []
# db/vector_store.py

import faiss
import os
import pickle
from typing import List
from config import settings
import numpy as np

class FaissVectorStore:
    def __init__(self, dim: int, persist_path: str = settings.VECTOR_DB_PATH):
        self.dim = dim
        self.persist_path = persist_path
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []  # List[str]

        # Try to load existing index
        self._load()

    def add_documents(self, texts: List[str], vectors: List[List[float]]):
        vec_array = np.array(vectors).astype('float32')
        self.index.add(vec_array)
        self.texts.extend(texts)
        self._save()

    def search(self, query_vec: List[float], top_k: int = 5) -> List[str]:
        q = np.array([query_vec]).astype('float32')
        _, I = self.index.search(q, top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def _save(self):
        if self.persist_path is None:
            return  # Don't persist in-memory stores
        faiss.write_index(self.index, os.path.join(self.persist_path, "index.faiss"))
        with open(os.path.join(self.persist_path, "texts.pkl"), "wb") as f:
            pickle.dump(self.texts, f)

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []

    def _load(self):
        if self.persist_path is None:
            return  # Skip loading for in-memory stores
        try:
            index_path = os.path.join(self.persist_path, "index.faiss")
            text_path = os.path.join(self.persist_path, "texts.pkl")
            if os.path.exists(index_path) and os.path.exists(text_path):
                self.index = faiss.read_index(index_path)
                with open(text_path, "rb") as f:
                    self.texts = pickle.load(f)
                print(f"✅ Loaded FAISS vector store from {self.persist_path}")
        except Exception as e:
            print(f"⚠️ Failed to load vector store: {e}")


