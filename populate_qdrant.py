from rest.clients.qdrant import QdrantClient
import json


# Load data
with open("data/qdrant_points.json", "r") as file:
    emb = json.load(file)


qdrant_client = QdrantClient(host="http://localhost")

# Create Qdrant collection
qdrant_client.create_collection(collection_name="dandi_collection")

# Populate collection with points
qdrant_client.add_points_to_collection(collection_name="dandi_collection", embeddings_objects=emb)

info = qdrant_client.get_collection_info("dandi_collection")
print(f"Inserted {info['points_count']} points to Qdrant collection")