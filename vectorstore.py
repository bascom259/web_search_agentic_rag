from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(texts):

    return model.encode(
        texts,
        normalize_embeddings=True
    )


class VectorStore:

    def __init__(self, dim):

        self.index = faiss.IndexFlatL2(dim)
        self.texts = []


    def add(self, embeddings, texts):

        self.index.add(np.array(embeddings))
        self.texts.extend(texts)


    def search(self, query_embedding, k=5):

        _, I = self.index.search(
            np.array([query_embedding]),
            k
        )

        return [
            self.texts[i]
            for i in I[0]
            if i < len(self.texts)
        ]