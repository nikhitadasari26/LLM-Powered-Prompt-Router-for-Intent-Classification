import os
import sys
import asyncio
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from router import Router

app = FastAPI(title="LLM-Powered Prompt Router")
router = Router()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = await router.process_message(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_cli():
    print("\n--- LLM-Powered Prompt Router CLI ---")
    print("Type your message and press Enter. Type 'exit' to quit.")
    print("Use @intent to override (e.g., @code, @data, @writing, @career).\n")
    
    while True:
        try:
            message = input("You: ").strip()
            if message.lower() in ["exit", "quit", "q"]:
                break
            if not message:
                continue
                
            result = await router.process_message(message)
            
            print(f"\n[Intent: {result['intent']} | Confidence: {result['confidence']:.2f}]")
            print(f"Expert: {result['response']}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-Powered Prompt Router")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--port", type=int, default=8000, help="Port for the web server")
    args = parser.parse_args()

    if args.cli:
        asyncio.run(run_cli())
    else:
        print(f"Starting web server on http://localhost:{args.port}")
        uvicorn.run(app, host="0.0.0.0", port=args.port)
