from flask import Flask, request, jsonify
from model import analyze_sentiment

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    result = analyze_sentiment(text)

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
