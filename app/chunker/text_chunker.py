

from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import settings

# Initialize a reusable splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,  ##chunk size 512 tokens
    chunk_overlap=settings.CHUNK_OVERLAP, #
    separators=["\n\n", "\n", " ", "","\n___+\n","\n---+\n","\n\\*\\*\\*+\n","```\n", "\n#{1,6}"]
)

def chunk_text(text: str) -> list[str]:
    """
    Splits the input text (plain or Markdown) into overlapping
    character-based chunks, using the settings from config.py.

    Returns a list of text chunks.
    """
    if not text:
        return []
    return splitter.split_text(text)

# chunker/text_chunker.py

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# #from config import settings
# from typing import List

# # 1) Set up a splitter with extra separators for markdown semantics
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=2000,#settings.CHUNK_SIZE,        # e.g. 2000 chars ≃ 500 tokens
#     chunk_overlap=100,#settings.CHUNK_OVERLAP,  # e.g. 200 chars ≃ 50 tokens
#     # Try splits at paragraphs, headings, code fences, separators...
#     separators=[
#         "\n\n",        # paragraph
#         "\n---\n",     # horizontal rule
#         "\n___\n",     # horizontal rule variant
#         "\n***\n",     # horizontal rule variant
#         "```",         # code fence
#         "\n#",         # markdown heading
#         "\n",          # line break
#         " ",           # space
#         ""             # fallback to char
#     ]
# )

# def _adjust_natural_boundaries(chunks: List[str], max_size: int, threshold: float = 0.8) -> List[str]:
#     """
#     For any chunk that still ends mid-sentence/paragraph (and is >= threshold*max_size),
#     look backwards for a '.', '\n\n' or '\n' past the threshold point and split there.
#     """
#     out: List[str] = []
#     for chunk in chunks:
#         if len(chunk) >= max_size and not chunk.endswith(("\n", ".", "?", "!")):
#             # look for best split point
#             candidates = [
#                 chunk.rfind("\n\n"),
#                 chunk.rfind(". "),
#                 chunk.rfind("\n")
#             ]
#             split_idx = max(candidates)
#             if split_idx > max_size * threshold:
#                 head = chunk[: split_idx + 1].rstrip()
#                 tail = chunk[split_idx + 1 :].lstrip()
#                 out.append(head)
#                 if tail:
#                     out.append(tail)
#                 continue
#         out.append(chunk)
#     return out

# def chunk_text(text: str) -> List[str]:
#     """
#     1. Recursively split text into char-based chunks using rich separators.
#     2. Post-process to enforce natural breakpoints for any leftover large chunks.
#     """
#     if not text:
#         return []
#     # Step 1: initial split
#     raw_chunks = splitter.split_text(text)
#     # Step 2: natural boundary adjustment
#     adjusted = _adjust_natural_boundaries(raw_chunks, 2000)
#     return adjusted
