import faiss
import numpy as np
import os
import pickle

INDEX_FILE = "memory.index"
META_FILE = "memory.pkl"
DIMENSION = 384

if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
    index = faiss.read_index(INDEX_FILE)

    with open(META_FILE, "rb") as f:
        metadata = pickle.load(f)
else:
    index = faiss.IndexFlatL2(DIMENSION)
    metadata = []


def save_index():
    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)


def add_memory(embedding, data):
    vector = np.array([embedding]).astype("float32")

    index.add(vector)
    metadata.append(data)

    save_index()


def search_memory(embedding, k=2):
    if len(metadata) == 0:
        return []

    vector = np.array([embedding]).astype("float32")

    distances, indices = index.search(vector, k)

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(metadata):
            item = metadata[idx]
            item["distance"] = float(dist)
            results.append(item)

    return results