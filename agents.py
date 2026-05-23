from llm import ask_llm
from tools import search_web, scrape_page, chunk_text
from vectorstore import VectorStore, embed


# -----------------------------
# Planner Agent
# -----------------------------
def planner_agent(state):

    query = state["query"]

    prompt = f"""
    Break this into 3 effective web search queries:

    {query}
    """

    queries = ask_llm(prompt).split("\n")

    queries = [
        q.strip()
        for q in queries
        if q.strip()
    ]

    state["queries"] = queries

    return state


# -----------------------------
# Research Agent
# -----------------------------
def researcher_agent(state):

    if state.get("skip_web", False):
        state["docs"] = []
        return state

    queries = state["queries"]

    urls = []

    for q in queries:
        urls += search_web(q)

    urls = list(set(urls))[:5]

    docs = [
        (u, scrape_page(u))
        for u in urls
    ]

    docs = [
        (u, d)
        for u, d in docs
        if d.strip() != ""
    ]

    state["docs"] = docs

    return state


# -----------------------------
# Retriever Agent
# -----------------------------
def retriever_agent(state):

    if state.get("skip_web", False):
        state["context"] = []
        state["sources"] = []
        return state

    query = state["query"]
    docs = state["docs"]

    chunks = []
    sources = []

    for url, doc in docs:
        c = chunk_text(doc)
        chunks += c
        sources += [url] * len(c)

    if len(chunks) == 0:
        state["context"] = []
        state["sources"] = []
        return state

    embeddings = embed(chunks)

    store = VectorStore(len(embeddings[0]))
    store.add(embeddings, chunks)

    query_emb = embed([query])[0]

    results = store.search(query_emb, k=2)

    state["context"] = results
    state["sources"] = list(set(sources[:2]))

    return state


# -----------------------------
# Answer Agent
# -----------------------------
def answer_agent(state):

    query = state["query"]
    context = state.get("context", [])[:2]
    memories = state.get("memories", [])[:2]

    memory_text = "\n".join([
        f"Previous Q: {m['query']}\nPrevious A: {m['answer']}"
        for m in memories
    ])

    prompt = f"""
    Answer the current question clearly.

    Use previous memory if relevant.
    Use web context if available.

    Previous Relevant Memories:
    {memory_text}

    Web Context:
    {' '.join(context)}

    Current Question:
    {query}
    """

    answer = ask_llm(prompt)

    state["answer"] = answer

    return state


# -----------------------------
# Critic Agent
# -----------------------------
def critic_agent(state):

    # prevent infinite loops
    state["iterations"] = state.get("iterations", 0) + 1

    if state["iterations"] >= 2:
        state["critique"] = "OK"
        return state

    query = state["query"]
    answer = state["answer"]

    prompt = f"""
    Evaluate this answer.

    If answer is good → say OK

    If answer needs improvement → say IMPROVE

    Question:
    {query}

    Answer:
    {answer}
    """

    critique = ask_llm(prompt)

    state["critique"] = critique

    return state