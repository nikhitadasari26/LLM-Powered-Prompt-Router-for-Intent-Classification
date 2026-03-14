import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup basic logging for console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Router:
    def __init__(self, prompts_path: str = "prompts.json"):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.log_file = os.getenv("LOG_FILE", "route_log.jsonl")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        with open(prompts_path, "r") as f:
            self.config = json.load(f)
            
    async def classify_intent(self, message: str) -> Dict[str, Any]:
        """Classifies the user message into an intent using an initial LLM call."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.config["classifier"]["system_prompt"]},
                    {"role": "user", "content": message}
                ],
                temperature=0
            )
            
            content = response.choices[0].message.content.strip()
            
            # Strip markdown code fences if present
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            intent_data = json.loads(content.strip())
            
            # Basic validation
            if "intent" not in intent_data or "confidence" not in intent_data:
                 return {"intent": "unclear", "confidence": 0.0}
            
            # Ensure intent is within allowed labels
            if intent_data["intent"] not in self.config["classifier"]["labels"]:
                 intent_data["intent"] = "unclear"
                 
            return intent_data
            
        except Exception as e:
            logger.error(f"Error in classify_intent: {e}")
            return {"intent": "unclear", "confidence": 0.0}

    async def route_and_respond(self, message: str, intent_data: Dict[str, Any]) -> str:
        """Routes the message to the appropriate expert persona and generates a response."""
        intent = intent_data.get("intent", "unclear")
        confidence = intent_data.get("confidence", 0.0)
        
        # Implement confidence threshold
        if confidence < 0.7 or intent == "unclear":
            return self.config["unclear"]["response"]
            
        persona = self.config["personas"].get(intent)
        if not persona:
            return self.config["unclear"]["response"]
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": persona["system_prompt"]},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in route_and_respond: {e}")
            return "I encountered an error while processing your request. Please try again later."

    async def log_request(self, user_message: str, intent_data: Dict[str, Any], final_response: str):
        """Logs the routing decision and response to a JSON Lines file."""
        log_entry = {
            "intent": intent_data.get("intent"),
            "confidence": intent_data.get("confidence"),
            "user_message": user_message,
            "final_response": final_response
        }
        
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error(f"Error writing to log file: {e}")

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Full pipeline: classify -> route -> log -> return."""
        # Check for manual override (Stretch Goal)
        manual_intent = None
        if message.startswith("@"):
            parts = message.split(" ", 1)
            label = parts[0][1:].lower()
            if label in self.config["personas"]:
                manual_intent = label
                message = parts[1] if len(parts) > 1 else ""

        if manual_intent:
            intent_data = {"intent": manual_intent, "confidence": 1.0, "manual": True}
        else:
            intent_data = await self.classify_intent(message)
            
        final_response = await self.route_and_respond(message, intent_data)
        await self.log_request(message if not manual_intent else f"@{manual_intent} {message}", intent_data, final_response)
        
        return {
            "intent": intent_data["intent"],
            "confidence": intent_data["confidence"],
            "response": final_response
        }
