"""
Core router module for the LLM-powered prompt router.
Handles intent classification, expert routing, and request logging.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "llama-3.1-8b-instant"
LOG_FILE = "route_log.jsonl"


def append_to_log(log_entry):
    """Appends a single JSON log entry to the route_log.jsonl file."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except IOError as err:
        print(f"Error writing to log: {err}")


def classify_intent(message):
    """
    Classifies the user's message into an intent category using a lightweight LLM call.
    Returns a dict with 'intent' and 'confidence' keys.
    Defaults to {'intent': 'unclear', 'confidence': 0.0} on any parsing failure.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.0,
        )

        reply = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model wraps JSON in them
        if reply.startswith("```json"):
            reply = reply[7:]
        elif reply.startswith("```"):
            reply = reply[3:]
        if reply.endswith("```"):
            reply = reply[:-3]

        intent_data = json.loads(reply.strip())

        if "intent" in intent_data and "confidence" in intent_data:
            valid_labels = ["code", "data", "writing", "career", "unclear"]
            if intent_data["intent"] not in valid_labels:
                intent_data["intent"] = "unclear"
            return intent_data
        else:
            raise ValueError("Missing 'intent' or 'confidence' keys in JSON")

    except Exception as err:
        print(f"Classification error: {err}")
        return {"intent": "unclear", "confidence": 0.0}


def route_and_respond(message, intent_data):
    """
    Routes the message to the appropriate expert persona and generates a response.
    If the intent is 'unclear', returns a clarifying question.
    Logs every request to route_log.jsonl.
    """
    intent_label = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)

    final_response = ""

    if intent_label == "unclear" or intent_label not in SYSTEM_PROMPTS:
        final_response = (
            "I'm not quite sure what you need. "
            "Are you asking for help with coding, data analysis, writing, or career advice?"
        )
    else:
        system_prompt = SYSTEM_PROMPTS[intent_label]
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
            )
            final_response = response.choices[0].message.content
        except Exception as err:
            final_response = f"An error occurred while generating the expert response: {err}"

    log_entry = {
        "intent": intent_label,
        "confidence": confidence,
        "user_message": message,
        "final_response": final_response,
    }
    append_to_log(log_entry)

    return final_response
