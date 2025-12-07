import os
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient
from openai import AsyncOpenAI
from fastapi.responses import StreamingResponse
import asyncio

# --- Configuration ---
def load_config():
    """Loads configuration from config.json"""
    try:
        script_dir = Path(__file__).parent
        config_path = script_dir / 'config.json'
        with open(config_path, 'r') as f:
            config = json.load(f)
        config.setdefault("QDRANT_COLLECTION_NAME", "physical_ai_book_v2")
        return config
    except FileNotFoundError:
        print("FATAL: config.json not found. Please copy config.json.example to config.json and fill in your credentials.")
        exit(1)
    except json.JSONDecodeError:
        print("FATAL: Could not decode config.json. Please ensure it is a valid JSON file.")
        exit(1)

config = load_config()

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Physical AI Textbook RAG Chatbot",
    description="A chatbot that answers questions based on the Physical AI & Humanoid Robotics textbook.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- API Clients ---
try:
    qdrant_client = QdrantClient(
        url=config["QDRANT_URL"],
        api_key=config["QDRANT_API_KEY"],
    )
    openai_client = AsyncOpenAI(api_key=config["OPENAI_API_KEY"])
    qdrant_collection_name = config["QDRANT_COLLECTION_NAME"]
except KeyError as e:
    print(f"FATAL: Missing required key in config.json: {e}")
    exit(1)
except Exception as e:
    print(f"Error initializing API clients: {e}")
    exit(1)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    query: str
    selected_text: str | None = None

# --- Core RAG Logic ---
async def get_relevant_context(query: str, limit: int = 5) -> list[dict]:
    """Queries Qdrant to find the most relevant text chunks for a given query."""
    try:
        print(f"DEBUG: Searching Qdrant collection: '{qdrant_collection_name}' for query: '{query}'")
        query_embedding_response = await openai_client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"
        )
        query_embedding = query_embedding_response.data[0].embedding

        search_results = qdrant_client.search(
            collection_name=qdrant_collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True,
            score_threshold=0.7 # Add a score threshold to filter less relevant results
        )
        
        print(f"DEBUG: Qdrant search returned {len(search_results)} results.")
        context = []
        for i, point in enumerate(search_results):
            payload = point.payload
            context.append(
                {"text": payload.get("text", ""), "source": payload.get("source", "Unknown")}
            )
            print(f"DEBUG: Result {i+1} - Score: {point.score:.2f}, Source: {payload.get('source')}, Text (start): {payload.get('text', '')[:100]}...")
        return context
    except Exception as e:
        print(f"Error getting context from Qdrant: {e}")
        return []

# --- API Endpoints ---
@app.get("/", summary="Health Check")
def read_root():
    return {"status": "ok", "message": "Welcome to the RAG Chatbot API"}

@app.post("/api/chat", summary="Handle Chat Queries")
async def chat_handler(request: ChatRequest):
    """
    Handles chatbot queries. Supports RAG mode (searching the book) and 
    selected-text mode (using user-highlighted text as context).
    The response is streamed back to the client.
    """
    context_str = ""
    sources = []

    if request.selected_text:
        context_str = request.selected_text
        sources = ["User-selected text"]
        print("INFO: Using user-selected text as context.")
    else:
        print(f"INFO: Performing RAG search for query: '{request.query}'")
        relevant_context = await get_relevant_context(request.query)
        print(f"DEBUG: get_relevant_context returned {len(relevant_context)} context items.")
        if relevant_context:
            context_str = "\n\n---\n\n".join([item['text'] for item in relevant_context])
            sources = sorted(list(set([item['source'] for item in relevant_context])))
            print(f"DEBUG: Context string sent to LLM (first 500 chars): {context_str[:500]}...")
        else:
            context_str = "No relevant context was found in the book to answer this question."
            print("DEBUG: No relevant context found from Qdrant.")
    
    # Construct the prompt for the LLM
    if context_str and context_str != "No relevant context was found in the book to answer this question.":
        system_prompt = (
            "You are a helpful AI assistant specializing in the Physical AI and Humanoid Robotics textbook. "
            "Answer the user's question concisely and professionally, based solely on the provided context. "
            "If the question cannot be answered from the context, state 'I cannot answer this question from the provided information.' "
            "Cite your sources using the format [Source: <source_name>].\n\n"
            f"Context:\n{context_str}\n\n"
            f"Sources: {', '.join(sources)}\n" if sources else ""
        )
    else:
        system_prompt = (
            "You are a helpful AI assistant. Answer the user's question concisely and professionally. "
            "If you don't know the answer, state 'I don't know.'\n\n"
        )

    user_message = request.query

    async def generate_stream():
        try:
            stream = await openai_client.chat.completions.create(
                model="gpt-4", # Or your preferred model, e.g., "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            # After streaming the answer, also send the sources
            if sources:
                yield f"\n\nSources: {', '.join(sources)}"

        except Exception as e:
            print(f"Error during LLM streaming: {e}")
            yield f"Error: {e}"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # Allow the host and port to be configured if needed
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)

