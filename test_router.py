import asyncio
import os
import time
from router import Router

# Sample test messages from the requirements
TEST_CASES = [
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
    print("Starting tests...")
    
    router = Router()
    
    for i, message in enumerate(TEST_CASES, 1):
        print(f"\n--- Test {i}/{len(TEST_CASES)} ---")
        print(f"Message: {message}")
        
        try:
            result = await router.process_message(message)
            print(f"Classified Intent: {result['intent']} (Confidence: {result['confidence']})")
            print(f"Response snippet: {result['response'][:150]}...\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        await asyncio.sleep(1)
    
    print("Tests complete. Check route_log.jsonl for output.")

if __name__ == "__main__":
    asyncio.run(run_tests())
