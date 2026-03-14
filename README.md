# LLM‑Powered Prompt Router for Intent Classification

An intelligent **LLM-powered routing system** that classifies user
intent and forwards the request to specialized AI expert personas.\
This architecture follows a **"Classify → Route → Respond"** pattern
used in modern AI systems to produce higher‑quality responses than
monolithic prompts.

------------------------------------------------------------------------

# Architecture Overview

The system performs two main steps:

1️⃣ **Intent Classification** - A lightweight LLM prompt classifies the
user's message. - The response must be structured JSON:

``` json
{
  "intent": "code",
  "confidence": 0.92
}
```

2️⃣ **Prompt Routing** - Based on the detected intent, the request is
routed to a specialized expert persona. - Each persona has its own
system prompt optimized for that task.

3️⃣ **Response Generation** - A second LLM call generates the final
answer using the selected expert persona.

4️⃣ **Logging** - Every request is logged to `route_log.jsonl` for
observability.

------------------------------------------------------------------------

# Supported Intents

  Intent    Expert Persona   Description
  --------- ---------------- -----------------------------------------------
  code      Code Expert      Helps with programming problems and debugging
  data      Data Analyst     Interprets datasets and suggests analysis
  writing   Writing Coach    Improves clarity, tone, and structure
  career    Career Advisor   Gives actionable career guidance
  unclear   Clarification    Asks the user to clarify the request

------------------------------------------------------------------------

# Features

Intent classification using LLM\
Confidence threshold routing (0.7)\
Four expert AI personas\
JSON structured responses\
Automatic request logging\
CLI mode for terminal interaction\
Modern web chat UI\
Docker container support\
Error handling for malformed JSON\
Manual intent override (`@code`, `@writing`, etc.)

------------------------------------------------------------------------

# Project Structure

    .
    ├── app.py
    ├── router.py
    ├── prompts.json
    ├── test_router.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.example
    ├── route_log.jsonl
    ├── index.html
    └── README.md

------------------------------------------------------------------------

# Prerequisites

-   Docker
-   Docker Compose
-   Python 3.10+
-   OpenAI API Key

------------------------------------------------------------------------

# Environment Setup

Create a `.env` file in the project root:

``` env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
LOG_FILE=route_log.jsonl
```

⚠️ Never commit your real API key to GitHub.

------------------------------------------------------------------------

# Running with Docker (Recommended)

Build and run the application:

``` bash
docker-compose up --build
```

After startup, open:

    http://localhost:8000

------------------------------------------------------------------------

# Running Locally

Install dependencies:

``` bash
pip install -r requirements.txt
```

Start the server:

``` bash
python app.py
```

Open in browser:

    http://localhost:8000

------------------------------------------------------------------------

# CLI Mode

Run the router directly in the terminal:

``` bash
python app.py --cli
```

Example:

    You: how do I sort a list in python?
    Router Intent: code (0.94)
    Response: ...

------------------------------------------------------------------------

# Running Tests

The project includes **15 required test messages** to validate routing
behavior.

Run:

``` bash
python test_router.py
```

Example test cases:

-   how do i sort a list of objects in python?
-   explain this sql query
-   help me improve this paragraph
-   career advice for software engineers
-   what's the average of these numbers
-   fix this bug pls

------------------------------------------------------------------------

# Logging

Every request is saved to:

    route_log.jsonl

Example log entry:

``` json
{
  "intent": "code",
  "confidence": 0.91,
  "user_message": "how do I sort a list in python",
  "final_response": "Use the built-in sorted() function..."
}
```

This provides **observability and debugging capability**.

------------------------------------------------------------------------

# Error Handling

The classifier may sometimes return invalid JSON.\
The system handles this safely:

    {
      "intent": "unclear",
      "confidence": 0.0
    }

The router then asks the user for clarification.

------------------------------------------------------------------------

# Manual Intent Override

Users can bypass classification using prefixes:

    @code fix this bug
    @writing improve this paragraph
    @career help me choose a career

This directly routes the message to the selected persona.

------------------------------------------------------------------------

# System Design Highlights

This project demonstrates several **production AI design patterns**:

-   Prompt routing architecture
-   Intent classification using LLMs
-   Structured JSON outputs
-   Confidence thresholding
-   Expert prompt specialization
-   Observability through logging
-   Containerized deployment

------------------------------------------------------------------------

# Example Workflow

User Input:

    how do i sort a list in python?

Classifier Output:

``` json
{
 "intent": "code",
 "confidence": 0.94
}
```

Router:

    Code Expert Persona Selected

Final Response:

    Python provides sorted() and list.sort() methods...

------------------------------------------------------------------------

# Future Improvements

Possible enhancements:

-   Add more expert personas
-   Support multiple LLM providers
-   Add conversation memory
-   Improve UI with streaming responses
-   Add analytics dashboard

------------------------------------------------------------------------
