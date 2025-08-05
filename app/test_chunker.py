# scripts/test_chunker.py
from parser.document_parser import get_document_text
from chunker.text_chunker import chunk_text

# 1. Download and extract plain text
url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
text = get_document_text(url, mode="markdown")

# 2. Chunk it
chunks = chunk_text(text)
print(f"Total chunks: {len(chunks)}")
print("First chunk preview:\n", chunks[0][:300], "...\n")

for i in chunks:
    #print length of each chunk
    print(f"Chunk length: {len(i)} characters")