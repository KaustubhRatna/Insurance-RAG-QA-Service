from rag.rag_system import generate_prompts

#question = "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
# question = "What is the waiting period for pre-existing diseases (PED) to be covered?"
question = ["How does the policy define a 'Hospital'"]
doc = ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"]
response = generate_prompts(doc,question)

print("\n🧠 Final Answer:\n", response)
