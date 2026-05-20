from fastapi import FastAPI
from pydantic import BaseModel

from embedding import get_embedding
from qdrant_service import search_vector

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/search")
def search(req: QueryRequest):

    # 1. Convert query to embedding
    query_vector = get_embedding(req.query)

    # 2. Search in Qdrant
    results = search_vector(query_vector, "stored_procedures")

    # 3. Format response
    response = []
    for r in results:
        response.append({
            "score": r.score,
            "stored_procedure": r.payload
        })

    return {"results": response}

class SearchRequest(BaseModel):
    query: str


@app.post("/searchDocs")
def search_docs(req: SearchRequest):
    query_vector = get_embedding(
        f"query: {req.query}"
    )

    results = search_vector(query_vector, "faq_documents")

    response = []

    for r in results:

        response.append({
            "score": r.score,
            "text": r.payload["text"]
        })

    return response