import qdrant_client
try:
    print(f"Qdrant Client Version: {qdrant_client.__version__}")
except AttributeError:
    print("qdrant_client has no __version__ attribute. Likely a very old version.")

try:
    client = qdrant_client.QdrantClient(":memory:")
    print(f"Has search? {hasattr(client, 'search')}")
    print(f"Has query? {hasattr(client, 'query')}")
    print(f"Client methods: {[m for m in dir(client) if not m.startswith('_')]}")
except Exception as e:
    print(f"Error inspecting client: {e}")

