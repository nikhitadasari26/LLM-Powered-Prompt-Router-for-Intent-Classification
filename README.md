# LLM-Powered Prompt Router for Intent Classification

This project is a Python service that intelligently routes user requests to specialized AI personas using a two-step LLM process (Classify, then Respond). It demonstrates intent-based routing to provide specialized, context-aware responses using the Groq API.

## Core Features

1. **Intent Classification**: Uses a fast LLM call to classify user intents into `code`, `data`, `writing`, `career`, or `unclear` and returns a JSON object with `intent` and `confidence`.
2. **Context-Aware Routing**: Routes the user's message to a specialized expert system prompt based on the classified intent.
3. **Graceful Handling of Unclear Intent**: If the intent is `unclear` or JSON parsing fails, the system safely asks the user a clarifying question instead of hallucinating.
4. **Structured JSONL Logging**: Logs all classifier inputs, outputs, classification confidence, and final responses to `route_log.jsonl`.

## Application Structure

- **prompts.py**: Defines the system personas (Code, Data, Writing, Career) and the classifier prompt.
- **router.py**: Contains the core `classify_intent` and `route_and_respond` functions, along with logging logic to `route_log.jsonl`.
- **app.py**: A Flask server with a `/api/route` REST endpoint for processing messages.
- **test_router.py**: A script containing 15 diverse test cases to evaluate the routing behavior out of the box.

## Setup Instructions

### Environment Setup

1. Clone the repository.
2. Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_groq_api_key_here
```

> **Note:** This project uses the Groq API (which is OpenAI-compatible). Get a free API key from [console.groq.com](https://console.groq.com).

### Running with Docker (Recommended)

```bash
docker-compose up --build
```

The API server will be accessible at `http://localhost:3001`.

### Running Locally without Docker

```bash
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:3000`.

### Running Tests

```bash
python test_router.py
```

This runs 15 diverse test cases and logs all results to `route_log.jsonl`.

### API Usage

Send a POST request to `/api/route`:

```bash
curl -X POST http://localhost:3000/api/route -H "Content-Type: application/json" -d '{"message": "how do I sort a list in python?"}'
```

## Design Decisions

- **Groq API**: Chosen for its speed and free tier, using the `llama-3.1-8b-instant` model.
- **Synchronous Architecture**: Keeps the codebase simple and easy to understand.
- **Separate Prompts Module**: System prompts are defined in `prompts.py` for easy modification and testing.
- **JSON Fence Stripping**: The classifier handles markdown-wrapped JSON responses gracefully.
- **JSONL Logging**: Every request is appended to `route_log.jsonl` for observability and debugging.
