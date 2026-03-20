#Phase 2.3 Websocket 
'''from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("""
    <html>
        <body>
            <h1>WebSocket Chat</h1>
            <form id="form">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id="messages"></ul>
            <script>
                const ws = new WebSocket("ws://localhost:8000/chat");
                ws.onmessage = function(event) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('li');
                    message.textContent = event.data;
                    messages.appendChild(message);
                };
                document.getElementById('form').onsubmit = function(event) {
                    event.preventDefault();
                    const input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = '';
                };
            </script>
        </body>
    </html>
    """)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Echo back the message with a prefix
        await websocket.send_text(f"You said: {data}")
'''




#2 - Way communication 
'''
from fastapi import FastAPI, WebSocket

app = FastAPI()


connections = {
    "user1": None,
    "user2": None
}

@app.websocket("/user1")
async def user1_ws(websocket: WebSocket):
    await websocket.accept()
    connections["user1"] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            
            if connections["user2"]:
                await connections["user2"].send_text(f"User1: {data}")
    except Exception:
        connections["user1"] = None

@app.websocket("/user2")
async def user2_ws(websocket: WebSocket):
    await websocket.accept()
    connections["user2"] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            
            if connections["user1"]:
                await connections["user1"].send_text(f"User2: {data}")
    except Exception:
        connections["user2"] = None
'''

# Adding Streaming 


'''import asyncio
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Split into words and stream back one at a time
            for word in data.split():
                await websocket.send_text(word)
                await asyncio.sleep(0.5)  # delay between words
    except Exception:
        await websocket.close()'''


'''#API Versioning 
import asyncio
from fastapi import FastAPI, WebSocket

app = FastAPI()

#Ve pehla version h
@app.websocket("/v1/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            for word in data.split():
                await websocket.send_text(word)
                await asyncio.sleep(0.5)  
    except Exception:
        await websocket.close()

# Ye dusra version h
@app.get("/v1/search")
async def search(q: str):
    
    return {"query": q, "results": [f"Result for {q} #2"]}'''



#Rate Limiting 2/min

'''from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )



@app.get("/v1/ping")
@limiter.limit("2/minute")
async def ping(request: Request):
    return {"message": "pong"}
'''

#Health Check
'''import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/health")
async def health_check():
    
    status = {"api": "up", "llm_provider": "unreachable", "vector_db": "unreachable"}
    
   
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get("https://api.openai.com/v1/models")
            if resp.status_code == 200:
                status["llm_provider"] = "reachable"
    except:
        pass 

   
    try:
        
        status["vector_db"] = "reachable" 
    except:
        pass 
    return status
'''


# Phase 3.1 coverting a documents into embeddings and putting an faiss 

'''import numpy as np
import faiss
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    "Hello , I am Mukul Nagar."
    
] 


embeddings = model.encode(documents, convert_to_numpy=True)


dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


app = FastAPI()

@app.get("/v1/search")
async def search(query: str = Query(...), top_k: int = 5):
    # Embed query
    q_emb = model.encode([query], convert_to_numpy=True)
    # Search in FAISS
    distances, indices = index.search(q_emb, top_k)
    # Collect results
    results = [documents[i] for i in indices[0]]
    return {"query": query, "results": results}'''



#adding chromaDB 

'''from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")


documents = [
    "FastAPI is a modern web framework for building APIs with Python.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "Sentence Transformers provide easy methods to compute embeddings for sentences and paragraphs.",
    "ChromaDB and Pinecone are managed vector databases for production use.",
    "OpenAI provides APIs for embeddings, completions, and other language tasks."
]


client = chromadb.Client()


collection = client.get_or_create_collection(name="docs")


embeddings = model.encode(documents, convert_to_numpy=True).tolist()
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(documents))]
)


app = FastAPI()

@app.get("/v1/search")
async def search(query: str = Query(...), top_k: int = 5):
    # Embed query
    q_emb = model.encode([query], convert_to_numpy=True).tolist()
    # Query ChromaDB
    results = collection.query(
        query_embeddings=q_emb,
        n_results=top_k
    )
    return {"query": query, "results": results["documents"][0]}
'''

# Chunking 


#Phase 3.3 Reranker


'''import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

# --- Step 1: Load models ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")   # fast bi-encoder for retrieval
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")  # accurate reranker

# --- Step 2: Prepare dataset ---
documents = [
    "FastAPI is a modern Python framework for building APIs quickly.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "Page 3 Table:\nProduct | Price | Discount\nA | $100 | 10%\nB | $200 | 20%\nC | $300 | 30%",
    "def add(a, b): return a + b",
    "SELECT name, price FROM products WHERE price > 100;",
    "Shopping list:\n- Apples\n- Bananas\n- Carrots\n- Dates",
    "Steps to deploy:\n1. Build Docker image\n2. Push to registry\n3. Deploy with Kubernetes",
    "Quarterly report:\nQ1 | $1M\nQ2 | $1.2M",
    "ChromaDB and Pinecone are managed vector databases for production use.",
    "OpenAI provides APIs for embeddings, completions, and other language tasks."
]

# --- Step 3: Initialize ChromaDB ---
client = chromadb.Client()
collection = client.get_or_create_collection(name="docs")

# --- Step 4: Insert documents ---
embeddings = embedder.encode(documents, convert_to_numpy=True).tolist()
collection.add(documents=documents,
               embeddings=embeddings,
               ids=[str(i) for i in range(len(documents))])

# --- Step 5: Search pipeline ---
def search_pipeline(query, top_k=5):
    # A. Embed query
    q_emb = embedder.encode([query], convert_to_numpy=True).tolist()

    # B. Retrieve top-20 candidates
    results = collection.query(query_embeddings=q_emb, n_results=20)
    candidates = results["documents"][0]

    # C. Re-rank with cross-encoder
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs)

    # D. Sort and return top-5
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [doc for doc, score in ranked]

# --- Step 6: Try it ---
query = "What does the table on page 3 say about pricing?"
print("Query:", query)
print("Results:")
for r in search_pipeline(query, top_k=5):
    print("-", r)


'''


# Adding threshold = 0.7

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

# --- Step 1: Load models ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")   # fast bi-encoder for retrieval
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")  # accurate reranker

# --- Step 2: Prepare dataset ---
documents = [
    "FastAPI is a modern Python framework for building APIs quickly.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "Page 3 Table:\nProduct | Price | Discount\nA | $100 | 10%\nB | $200 | 20%\nC | $300 | 30%",
    "def add(a, b): return a + b",
    "SELECT name, price FROM products WHERE price > 100;",
    "Shopping list:\n- Apples\n- Bananas\n- Carrots\n- Dates",
    "Steps to deploy:\n1. Build Docker image\n2. Push to registry\n3. Deploy with Kubernetes",
    "Quarterly report:\nQ1 | $1M\nQ2 | $1.2M",
    "ChromaDB and Pinecone are managed vector databases for production use.",
    "OpenAI provides APIs for embeddings, completions, and other language tasks."
]

# --- Step 3: Initialize ChromaDB ---
client = chromadb.Client()
collection = client.get_or_create_collection(name="docs")

# --- Step 4: Insert documents ---
embeddings = embedder.encode(documents, convert_to_numpy=True).tolist()
collection.add(documents=documents,
               embeddings=embeddings,
               ids=[str(i) for i in range(len(documents))])

# --- Step 5: Search pipeline with threshold ---
def search_pipeline(query, top_k=5, threshold=0.7):
    # A. Embed query
    q_emb = embedder.encode([query], convert_to_numpy=True).tolist()

    # B. Retrieve top-20 candidates
    results = collection.query(query_embeddings=q_emb, n_results=20)
    candidates = results["documents"][0]

    # C. Re-rank with cross-encoder
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs)

    # D. Sort by score
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    # E. Apply threshold
    if ranked and ranked[0][1] < threshold:
        return "I don't have enough information to answer that."

    # F. Return top-k
    return [doc for doc, score in ranked[:top_k]]

# --- Step 6: Try it ---
#query = "What does the table on page 3 say about pricing?"
query = "Tell me about quantums "
print("Query:", query)
print("Results:", search_pipeline(query))
