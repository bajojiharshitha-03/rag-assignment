from flask import Flask, request, jsonify
from flask_cors import CORS
from retrieval import search_documents
from llm import generate_answer

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    # API Requirements: Validate input
    if not data or "message" not in data:
        return jsonify({"error": "Message field is required"}), 400
    
    user_query = data["message"]

    try:
        # Step 1: Retrieval (Happens before LLM call)
        context_chunks = search_documents(user_query)
        
        # Step 2: Generation
        answer = generate_answer(user_query, context_chunks)

        # Mandatory Response Format
        return jsonify({
            "answer": answer,
            "metadata": {
                "sources_found": len(context_chunks),
                "status": "success"
            }
        })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)