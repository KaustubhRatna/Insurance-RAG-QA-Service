# indexer/index_documents.py

import os
from typing import List
##
from chunker.text_chunker import chunk_text
from embedder.embed import embed_texts, get_embedding_dimension
from db.vector_store import FaissVectorStore
from config import settings
from parser.document_parser import parse_pdf_markdown, parse_pdf_plain

# Use local documents directory
DOCS_DIR = r"C:\Projects\SM _ insurance\baseline\rag_insurance\Domain Documents"
USE_MARKDOWN = True  # Toggle this if you want to switch to plain parsing

def index_local_documents() -> FaissVectorStore:
    """
    Parses and indexes all PDF documents in the local documents directory.
    Returns a persistent vector store.
    """
    dim = get_embedding_dimension()
    vector_store = FaissVectorStore(dim)

    for file in os.listdir(DOCS_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(DOCS_DIR, file)
        print(f"\n📄 Indexing: {file_path}")

        try:
            # Parse
            if USE_MARKDOWN:
                parsed_text = parse_pdf_markdown(file_path)
            else:
                with open(file_path, "rb") as f:
                    parsed_text = parse_pdf_plain(f.read())

            # Chunk
            chunks = chunk_text(parsed_text)
            print(f"🔹 Total chunks: {len(chunks)}")

            # Embed
            embeddings = embed_texts(chunks)

            # Add to FAISS
            vector_store.add_documents(chunks, embeddings)
            print("✅ Done.\n")

        except Exception as e:
            print(f"❌ Failed to index {file_path}: {e}")

    return vector_store

if __name__ == "__main__":
    store = index_local_documents()

    # Test with a query
    from embedder.embed import embed_query

    query = "What is the waiting period for cataract surgery?"
    q_vec = embed_query(query)
    results = store.search(q_vec, top_k=3)

    print("\n🔍 Top Matches:")
    for i, chunk in enumerate(results):
        print(f"\n--- Match {i+1} ---\n{chunk[:500]}\n")
