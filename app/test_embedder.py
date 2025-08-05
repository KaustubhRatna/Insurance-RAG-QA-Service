# scripts/test_local_embed.py

from embedder.embed import embed_texts, embed_query,get_max_input_tokens

chunks = ["Test chunk one.", "Test chunk two."]
vecs = embed_texts(chunks)
print("Chunk vectors shapes:", [len(v) for v in vecs])

qv = embed_query("When is knee surgery covered?")
print("Query vector length:", len(qv))

print("First chunk vector:", vecs[0]) 
print("First chunk vector:", vecs[1])

print("Max token length:", get_max_input_tokens())