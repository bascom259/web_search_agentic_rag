from sentence_transformers import SentenceTransformer
from faiss_store import add_memory, search_memory

memory_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    embedding = memory_model.encode(
        text,
        normalize_embeddings=True
    )
    return embedding.tolist()

def save_memory(query, answer):
    embedding = get_embedding(query)

    add_memory(
        embedding,
        {
            "query": query,
            "answer": answer
        }
    )

def retrieve_memories(query, k=2):
    embedding = get_embedding(query)
    return search_memory(embedding, k=k)