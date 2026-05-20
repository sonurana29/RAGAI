from qdrant_client import QdrantClient
from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("localhost", port=6333)

COLLECTION = "stored_procedures"

def create_collection(collectionname):
    client.recreate_collection(
        collection_name=collectionname,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

def insert_vector(id, vector, payload, collectionname):
    client.upsert(
        collection_name=collectionname,
        points=[
            {
                "id": id,
                "vector": vector,
                "payload": payload
            }
        ]
    )

def insert_points(points, collectionname):
    client.upsert(
        collection_name=collectionname,
        points=points
    )

def search_vector(query_vector, collectionname):
    results = client.query_points(
        collection_name=collectionname,
        query=query_vector,
        limit=3
    ).points

    return results

