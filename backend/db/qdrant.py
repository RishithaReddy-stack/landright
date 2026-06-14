import json
import uuid
import boto3
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from backend.core.config import settings


client = QdrantClient(url=settings.qdrant_url)
encoder = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge_from_s3() -> list:
    """Load knowledge base JSON from S3."""
    s3 = boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    response = s3.get_object(Bucket=settings.s3_bucket_name, Key="knowledge_base.json")
    return json.loads(response["Body"].read().decode("utf-8"))


def create_collection():
    existing = [c.name for c in client.get_collections().collections]
    if settings.collection_name not in existing:
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Created collection: {settings.collection_name}")
    else:
        print(f"Collection already exists: {settings.collection_name}")


def index_knowledge_base():
    """Load knowledge base from S3, embed it, and index into Qdrant."""
    knowledge_base = load_knowledge_from_s3()
    create_collection()

    points = []
    for item in knowledge_base:
        vector = encoder.encode(item["content"]).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "id": item["id"],
                "title": item["title"],
                "category": item["category"],
                "content": item["content"],
                "tags": item["tags"],
            },
        ))

    client.upsert(collection_name=settings.collection_name, points=points)
    print(f"Indexed {len(points)} documents into Qdrant")


def search(query: str, limit: int = 3):
    vector = encoder.encode(query).tolist()
    results = client.search(
        collection_name=settings.collection_name,
        query_vector=vector,
        limit=limit,
    )
    return [hit.payload for hit in results]


if __name__ == "__main__":
    index_knowledge_base()
