from typing import TypedDict

from langgraph.graph import StateGraph

from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding import get_embedding


from qdrant_service import insert_points

from qdrant_client import models


# Workflow State
class GraphState(TypedDict):

    document_text: str

    chunks: list

    embeddings: list


# NODE 1 — Chunking
def chunking_node(state):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(
        state["document_text"]
    )

    state["chunks"] = chunks

    return state


# NODE 2 — Embedding
def embedding_node(state):

    embeddings = []

    for chunk in state["chunks"]:

        vector = get_embedding(chunk)

        embeddings.append(vector)

    state["embeddings"] = embeddings

    return state


# NODE 3 — Store in Qdrant
def qdrant_node(state):

    points = []

    for idx, chunk in enumerate(state["chunks"]):

        points.append(
            models.PointStruct(
                id=idx,
                vector=state["embeddings"][idx],
                payload={
                    "text": chunk
                }
            )
        )

    insert_points(points,"faq_documents")

    return state


# Build Graph
workflow = StateGraph(GraphState)

workflow.add_node("chunking", chunking_node)

workflow.add_node("embedding", embedding_node)

workflow.add_node("qdrant", qdrant_node)

workflow.set_entry_point("chunking")

workflow.add_edge("chunking", "embedding")

workflow.add_edge("embedding", "qdrant")

graph = workflow.compile()