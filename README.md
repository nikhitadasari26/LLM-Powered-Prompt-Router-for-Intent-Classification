# LLM-Powered Prompt Router for Intent Classification

This project implements an intelligent routing service that classifies user messages into different intent categories and delegates them to specialized AI expert personas.

## Features
- **Intent Classification**: Uses a lightweight LLM call to detect user intent (Code, Data, Writing, Career) with confidence scores.
- **Specialized Personas**: Four distinct expert personas designed with specific system prompts to provide high-quality responses.
- **Dynamic Routing**: Automatically routes messages based on intent and confidence thresholds.
- **Glassmorphism Web UI**: A modern, responsive chat interface.
- **CLI Mode**: Direct interaction via terminal.
- **Observability**: Logs every routing decision and response to a JSON Lines file.
- **Containerized**: Fully Dockerized for easy deployment.

## Prerequisites
- Docker and Docker Compose
- OpenAI API Key

## Setup and Installation

### 1. Environment Configuration
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
LOG_FILE=route_log.jsonl
```

### 2. Running with Docker
The easiest way to run the application is using Docker Compose:
```bash
docker-compose up --build
```
The web interface will be available at `http://localhost:8000`.

### 3. Local Installation (Optional)
If you prefer to run it without Docker:
```bash
pip install -r requirements.txt
python app.py
```

### 4. Running the CLI
To interact with the router directly from your terminal:
```bash
python app.py --cli
```

### 5. Running Tests
To verify the routing logic with the 15 required test cases:
```bash
python test_router.py
```

## Design Overview
The system follows a "Classify, then Respond" pattern:
1. **Classifier**: A specific system prompt instructs the LLM to output a JSON object with `intent` and `confidence`.
2. **Router**: Based on the intent, the system selects the corresponding prompt from `prompts.json`.
3. **Thresholding**: If confidence is below 0.7 or intent is "unclear", it asks for clarification instead of guessing.
4. **Logging**: Every transaction is appended to `route_log.jsonl` for audit and debugging.
