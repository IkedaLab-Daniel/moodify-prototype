from flask import Flask, request, jsonify
from model import analyze_sentiment, moodify_text

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    result = analyze_sentiment(text)

    return jsonify(result)

@app.route("/moodify", methods=["POST"])
def moodify():
    data = request.get_json()

    if not data or "text" not in data or "target_sentiment" not in data:
        return jsonify({"error": "Missing 'text' or 'target_sentiment' in request body"}), 400

    text = data["text"]
    target_sentiment = data["target_sentiment"]
    
    result = moodify_text(text, target_sentiment)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
