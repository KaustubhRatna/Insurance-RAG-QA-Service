from parser.document_parser import get_document_text

url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
# Plain text extraction:
plain_text = get_document_text(url, mode="plain")

# Markdown extraction:
md_text = get_document_text(url, mode="markdown")
print("Plain Text Output:\n", plain_text)
print("Markdown Output:\n", md_text)