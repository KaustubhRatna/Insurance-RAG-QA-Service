from typing import List, Optional
from config import settings
from embedder.embed import embed_query, embed_texts, get_embedding_dimension
from db.vector_store import FaissVectorStore
from parser.document_parser import get_document_text
from chunker.text_chunker import chunk_text

def generate_prompts(
    document_url: Optional[str],
    questions: List[str]
) -> List[str]:
    # 1) Load persistent store (existing docs)
    persistent_store = FaissVectorStore(
        get_embedding_dimension(),
        persist_path=settings.VECTOR_DB_PATH
    )

    # 2) If there's a new document, parse/ chunk/ embed it once
    new_chunks: List[str] = []
    new_vecs: List[List[float]] = []
    if document_url:
        text = get_document_text(document_url, mode="markdown")
        all_new_chunks = chunk_text(text)
        # Filter out chunks already present in persistent store
        new_chunks = [c for c in all_new_chunks if c not in persistent_store.texts]
        new_vecs = embed_texts(new_chunks)

        # Build an in-memory FAISS index for just this new doc, only if we have new chunks
        if new_chunks:
            temp_store = FaissVectorStore(get_embedding_dimension(), persist_path=None)
            temp_store.clear()
            temp_store.add_documents(new_chunks, new_vecs)
        else:
            temp_store = None
    else:
        temp_store = None

    prompts: List[str] = []

    # 3) For each question, retrieve and assemble context
    for question in questions:
        qv = embed_query(question)

        if temp_store:
            top_new = temp_store.search(qv, top_k=3)
            top_existing = persistent_store.search(qv, top_k=2)
        else:
            top_new = []
            top_existing = persistent_store.search(qv, top_k=5)

        # Deduplicate
        seen = set()
        unique_new = [c for c in top_new if not (c in seen or seen.add(c))]
        unique_existing = [c for c in top_existing if not (c in seen or seen.add(c))]

        # Build context string
        if unique_new:
            context = (
                "The following context is extracted primarily from the **newly uploaded document**:\n\n"
                + "\n\n--Chunk_Start--\n\n".join(unique_new)
                + "\n\nThe following context is retrieved from the **existing indexed documents**:\n\n"
                + "\n\n--Chunk_Start--\n\n".join(unique_existing)
            )
        else:
            context = (
                "The following context is retrieved from the **existing indexed documents**:\n\n"
                + "\n\n--Chunk_Start--\n\n".join(unique_existing)
            )

        # Build the prompt
        prompt = f"""
You are an expert insurance assistant. Use only the provided document context to answer the question below.

Instructions:
- Base your answer strictly on the given context. Do not use outside knowledge.
- Keep the answers precise and relevant to the question. Do not add unnecessary information like disclaimers, etc.
- GIVE THE BEST POSSIBLE ANSWER BASED ON THE CONTEXT PROVIDED.
- Give A brief explanation for reaching a decision by utilizing the source documents/context.

Example Question and Answer for reference:
- Q: What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?
  A: A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.
- Q: What is the waiting period for pre-existing diseases (PED) to be covered?
  A: There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.
- Q: Are there any sub-limits on room rent and ICU charges for Plan A?
  A: Yes, for Plan A, the daily room rent is capped at 1% of the Sum Insured, and ICU charges are capped at 2% of the Sum Insured. These limits do not apply if the treatment is for a listed procedure in a Preferred Provider Network (PPN).

Document Context:
----------------
{context}
----------------

Question: {question}

Answer (based only on the above context):
"""
        prompts.append(prompt)

    # 4) After all prompts are built, update the persistent store once
    if document_url and settings.ALLOW_DB_UPDATE and new_chunks:
        print("📥 Persisting new document embeddings to main FAISS store...")
        persistent_store.add_documents(new_chunks, new_vecs)
        # If your FaissVectorStore exposes a ._save() or .persist() method:
        persistent_store._save()

    return prompts
