import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"

from fastapi import FastAPI
from graph import build_graph

from models import Base, ChatHistory
from database import engine, SessionLocal
from redis_client import redis_client

import json

# create SQL tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

graph = build_graph()


@app.get("/")
def home():

    return {
        "message": "Agentic RAG API Running"
    }


@app.post("/chat")
def chat(query: str):

    import json
    from memory import retrieve_memories, save_memory

    cached = redis_client.get(query)

    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")

    memories = retrieve_memories(query, k=2)

    skip_web = False

    if len(memories) > 0:
        best_distance = memories[0].get("distance", 999)

        if best_distance < 0.35:
            print("STRONG MEMORY HIT - SKIPPING WEB")
            skip_web = True

    result = graph.invoke({
        "query": query,
        "memories": memories,
        "skip_web": skip_web
    })

    response = {
        "answer": result["answer"],
        "sources": result.get("sources", [])
    }

    redis_client.set(
        query,
        json.dumps(response),
        ex=3600
    )

    save_memory(query, result["answer"])

    return response