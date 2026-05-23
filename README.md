# Agentic RAG System with Semantic Memory

An advanced Agentic Retrieval-Augmented Generation (RAG) system built using FastAPI, LangGraph, LangChain, FAISS, Redis, PostgreSQL, and Ollama.

The system supports:
- Multi-agent orchestration
- Web-augmented generation
- Semantic long-term memory
- Persistent memory retrieval
- Redis caching
- Local LLM inference using Ollama
- GPU acceleration
- Context-aware responses

---

# Architecture

User Query
↓
Redis Cache Check
↓
Semantic Memory Retrieval (FAISS)
↓
LangGraph Agent Workflow
↓
Web Search + Scraping
↓
Context Retrieval
↓
Ollama LLM Generation
↓
Persistent Memory Storage

---

# Features

- Agentic workflow using LangGraph
- Semantic memory using FAISS
- Long-term persistent memory
- Redis exact-query caching
- PostgreSQL chat history logging
- Web search and scraping pipeline
- Local LLM inference using Ollama
- GPU acceleration support
- FastAPI backend API
- Memory-aware contextual responses
- Automatic web-skip optimization using semantic similarity

---

# Tech Stack

## Backend
- FastAPI
- Uvicorn

## Agent Framework
- LangChain
- LangGraph
- AutoGen

## Vector Memory
- FAISS
- SentenceTransformers

## Database
- PostgreSQL

## Cache
- Redis

## LLM
- Ollama
- phi3:mini / mistral

## Embeddings
- all-MiniLM-L6-v2

---

# Project Structure

``` id="jlwm0g"
agentic_rag/
│
├── main.py
├── agents.py
├── graph.py
├── llm.py
├── tools.py
├── memory.py
├── faiss_store.py
├── embeddings.py
├── vector_store.py
├── database.py
├── models.py
├── config.py
├── requirements.txt
├── .env
│
├── memory.index
├── memory.pkl
│
└── README.md
