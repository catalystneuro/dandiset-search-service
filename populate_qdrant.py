from rest.clients.qdrant import QdrantClient
import json
import os


# Load data
with open("data/qdrant_points.json", "r") as file:
    emb = json.load(file)


qdrant_client = QdrantClient(
    host=os.environ.get("QDRANT_HOST", "http://localhost"),
    port=os.environ.get("QDRANT_PORT", 6333),
    vector_size=os.environ.get("QDRANT_VECTOR_SIZE", 1536),
    api_key=os.environ.get("QDRANT_API_KEY", None)
)

# Create Qdrant collection
qdrant_client.create_collection(collection_name="dandi_collection")

# Populate collection with points
qdrant_client.add_points_to_collection(collection_name="dandi_collection", embeddings_objects=emb)

info = qdrant_client.get_collection_info("dandi_collection")
print(f"Inserted {info['points_count']} points to Qdrant collection")