from flask import Flask, request, jsonify
from model import analyze_sentiment

app = Flask(__name__)

@app.route("/api/sentiment", methods=["POST"])
def sentiment():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    sentiment = analyze_sentiment(text)

    return jsonify({"sentiment": sentiment})

if __name__ == "__main__":
    app.run(port=5001)
