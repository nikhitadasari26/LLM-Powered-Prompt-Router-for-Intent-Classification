import asyncio
import os
import json
from router import Router

# Sample test messages from the requirements
TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

async def run_tests():
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY is not set. Tests will likely fail unless mocked.")
        # We could mock the responses here for demonstration if needed, 
        # but let's assume the user will run this with their key.
    
    router = Router()
    print(f"{'#':<3} | {'Intent':<10} | {'Conf':<6} | {'Message':<40}")
    print("-" * 70)
    
    for i, msg in enumerate(TEST_MESSAGES, 1):
        try:
            # We only run classification to avoid too many API calls if testing cost is a concern,
            # but the requirement says "Test your router", so we run the full process.
            result = await router.process_message(msg)
            print(f"{i:<3} | {result['intent']:<10} | {result['confidence']:>6.2f} | {msg[:37]}...")
        except Exception as e:
            print(f"{i:<3} | ERROR      |        | {msg[:37]}... ({e})")

if __name__ == "__main__":
    asyncio.run(run_tests())
