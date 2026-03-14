"""
Express-style API server for the LLM-powered prompt router.
Provides a REST endpoint for classifying and routing user messages.
"""

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from router import classify_intent, route_and_respond

load_dotenv()

app = Flask(__name__)
PORT = int(os.getenv("PORT", 3000))


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Prompt Router service is running!"})


@app.route("/api/route", methods=["POST"])
def route_message():
    try:
        data = request.get_json()
        message = data.get("message") if data else None

        if not message:
            return jsonify({"error": 'Please provide a "message" field in the JSON body.'}), 400

        intent_data = classify_intent(message)
        final_response = route_and_respond(message, intent_data)

        return jsonify({
            "original_message": message,
            "classification": intent_data,
            "response": final_response,
        })

    except Exception as err:
        print(f"Server error: {err}")
        return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    print(f"Server is running on http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT)
