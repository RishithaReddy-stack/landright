from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from backend.core.config import settings
from backend.knowledge.content import KNOWLEDGE_BASE
import uuid

client = QdrantClient(url=settings.qdrant_url)
encoder = SentenceTransformer("all-MiniLM-L6-v2")

def create_collection():
    existing = [c.name for c in client.get_collections().collections]
    if settings.collection_name not in existing:
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Created collection: {settings.collection_name}")
    else:
        print(f"Collection already exists: {settings.collection_name}")

def index_knowledge_base():
    create_collection()
    points = []
    for item in KNOWLEDGE_BASE:
        vector = encoder.encode(item["content"]).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "id": item["id"],
                "title": item["title"],
                "category": item["category"],
                "content": item["content"],
                "tags": item["tags"]
            }
        ))
    client.upsert(collection_name=settings.collection_name, points=points)
    print(f"Indexed {len(points)} documents into Qdrant")

def search(query: str, limit: int = 3):
    vector = encoder.encode(query).tolist()
    results = client.search(
        collection_name=settings.collection_name,
        query_vector=vector,
        limit=limit
    )
    return [hit.payload for hit in results]

if __name__ == "__main__":
    index_knowledge_base()