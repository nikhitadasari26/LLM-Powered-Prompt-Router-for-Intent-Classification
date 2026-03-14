"""
Test runner for the LLM-powered prompt router.
Runs 15 diverse test cases to validate classification and routing behavior.
"""

import time
from router import classify_intent, route_and_respond

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
    "My boss says my writing is too verbose.",
]


def run_tests():
    print("Starting tests...")

    for i, message in enumerate(TEST_CASES, 1):
        print(f"\n--- Test {i}/{len(TEST_CASES)} ---")
        print(f"Message: {message}")

        intent = classify_intent(message)
        print(f"Classified Intent: {intent['intent']} (Confidence: {intent['confidence']})")

        response = route_and_respond(message, intent)
        print(f"Response snippet: {response[:150]}...\n")

        time.sleep(1)

    print("Tests complete. Check route_log.jsonl for output.")


if __name__ == "__main__":
    run_tests()
