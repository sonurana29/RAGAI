from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/e5-small")

def get_embedding(text: str):
    # IMPORTANT for E5
    text = f"passage: {text}"
    return model.encode(text).tolist()