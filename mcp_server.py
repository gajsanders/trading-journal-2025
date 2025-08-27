import os
import glob
import threading
import logging
from typing import List, Optional

import tqdm
import requests
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Suppress noisy library outputs and progress bars ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["WANDB_DISABLED"] = "true"
os.environ["CHROMADB_TELEMETRY"] = "false"

try:
    tqdm.tqdm = tqdm.tqdm_class = lambda *a, **k: iter([])
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

# === CONFIG ===
PROJECT_PATH = "./"
COLLECTION_NAME = "codebase"
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen/qwen3-30b-a3b-2507"

# === EMBEDDINGS ===
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(
    COLLECTION_NAME, embedding_function=embedding_fn
)

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict = {}
    id: Optional[int] = None  # Make id optional for notifications

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: int
    result: Optional[dict] = None
    error: Optional[dict] = None

    class Config:
        exclude_none = True

def index_codebase():
    file_paths = glob.glob(os.path.join(PROJECT_PATH, "**/*.py"), recursive=True)
    for path in file_paths:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        for idx, chunk in enumerate(chunks):
            doc_id = f"{path}_{idx}"
            collection.upsert(
                documents=[chunk],
                ids=[doc_id],
                metadatas=[{"source": path}]
            )
    logging.info(f"Indexed {len(file_paths)} files into {COLLECTION_NAME}")

@app.post("/index")
async def index_route():
    index_codebase()
    return {"status": "Indexing complete"}

class CodebaseEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            logging.info(f"File changed: {event.src_path}, re-indexing...")
            index_codebase()

def start_watcher():
    observer = Observer()
    handler = CodebaseEventHandler()
    observer.schedule(handler, PROJECT_PATH, recursive=True)
    observer.start()
    logging.info("Watch mode started: monitoring codebase for changes.")
    return observer

@app.on_event("startup")
def startup_event():
    index_codebase()
    threading.Thread(target=start_watcher, daemon=True).start()

@app.post("/mcp")
async def mcp_endpoint(req: Request):
    try:
        payload = await req.json()
        mcp_req = MCPRequest(**payload)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid JSON-RPC request: {str(e)}"}
        )

    # Handle notifications (no id field, no response needed)
    if mcp_req.id is None:
        logging.info(f"Received notification: {mcp_req.method}")
        return JSONResponse(content={})

    if mcp_req.method == "initialize":
        response = MCPResponse(
            id=mcp_req.id,
            result={
                "protocolVersion": "2025-03-26",
                "serverInfo": {
                    "name": "my-mcp-server",
                    "version": "1.0",
                    "description": "Custom MCP server connected to LMStudio locally"
                },
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    },
                    "resources": {
                        "subscribe": False,
                        "listChanged": False
                    }
                }
            }
        )
        return JSONResponse(content=response.dict(exclude_none=True))

    elif mcp_req.method == "tools/list":
        response = MCPResponse(
            id=mcp_req.id,
            result={
                "tools": [
                    {
                        "name": "query_codebase",
                        "description": "Search and query the indexed codebase using semantic search",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query to find relevant code snippets"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        )
        return JSONResponse(content=response.dict(exclude_none=True))

    elif mcp_req.method == "tools/call":
        tool_name = mcp_req.params.get("name")
        tool_args = mcp_req.params.get("arguments", {})
        
        if tool_name == "query_codebase":
            query_text = tool_args.get("query")
            if not isinstance(query_text, str):
                response = MCPResponse(
                    id=mcp_req.id,
                    error={"code": -32602, "message": "Invalid params: 'query' string required"}
                )
                return JSONResponse(content=response.dict(exclude_none=True))

            results = collection.query(query_texts=[query_text], n_results=5)
            retrieved_contexts: List[str] = results["documents"][0]
            sources: List[str] = [m["source"] for m in results["metadatas"]]

            context = "\n---\n".join(retrieved_contexts)
            prompt = (
                f"Question:\n{query_text}\n\nRelevant code snippets:\n{context}\n\n"
                "Answer the question using only the context above if possible."
            )

            try:
                llm_payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "You are a helpful coding assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1024,
                }
                llm_response = requests.post(LMSTUDIO_API, json=llm_payload)
                llm_response.raise_for_status()
                completion = llm_response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                response = MCPResponse(
                    id=mcp_req.id,
                    error={"code": -32000, "message": f"LLM API request failed: {str(e)}"}
                )
                return JSONResponse(content=response.dict(exclude_none=True))

            response = MCPResponse(
                id=mcp_req.id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": f"Query: {query_text}\n\nAnswer: {completion}\n\nSources: {', '.join(sources)}"
                        }
                    ]
                }
            )
            return JSONResponse(content=response.dict(exclude_none=True))
        else:
            response = MCPResponse(
                id=mcp_req.id,
                error={"code": -32601, "message": f"Tool '{tool_name}' not found"}
            )
            return JSONResponse(content=response.dict(exclude_none=True))

    else:
        response = MCPResponse(
            id=mcp_req.id,
            error={"code": -32601, "message": f"Method '{mcp_req.method}' not found"}
        )
        return JSONResponse(content=response.dict(exclude_none=True))

@app.get("/v1/ready")
async def ready():
    return JSONResponse({"status": "ok"})

@app.get("/v1/context")
async def context_info():
    return JSONResponse({
        "name": "my-mcp-server",
        "version": "1.0",
        "description": "Custom MCP server connected to LMStudio locally"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server:app", host="127.0.0.1", port=8080, reload=False)
