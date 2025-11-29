import qdrant_client
print(f"Qdrant Client Version: {qdrant_client.__version__}")
try:
    client = qdrant_client.QdrantClient(":memory:")
    print(f"Has search? {hasattr(client, 'search')}")
except Exception as e:
    print(f"Error creating client: {e}")

