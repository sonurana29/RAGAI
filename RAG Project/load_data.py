from stored_procedures import stored_procedures
from embedding import get_embedding
from qdrant_store import create_collection, insert_vector

create_collection("stored_procedures")

for sp in stored_procedures:
    text = sp["name"] + " " + sp["description"]
    vector = get_embedding(text)

    insert_vector(
        id=sp["id"],
        vector=vector,
        payload=sp,
        collectionname="stored_procedures"
    )

print("Data loaded into Qdrant")