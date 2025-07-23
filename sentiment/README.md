# Sentiment Analysis Service

A Flask-based sentiment analysis service that provides both sentiment analysis and text transformation (moodification) capabilities using TextBlob and OpenRouter's DeepSeek model.

## Features

- **Sentiment Analysis**: Analyze text sentiment (positive, negative, neutral) with confidence scores
- **Moodify**: Transform text to match a target sentiment using AI (DeepSeek LLM via OpenRouter)
- **Fallback System**: Falls back to word replacement if LLM API fails

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

3. Run the service:
```bash
python app.py
```

The service will run on `http://127.0.0.1:5000`

## API Endpoints

### POST /predict
Analyze sentiment of text.

**Request:**
```json
{
  "text": "I love this beautiful day!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.8,
  "polarity": 0.7,
  "subjectivity": 0.6,
  "scores": {
    "positive": 0.7,
    "negative": 0.1,
    "neutral": 0.2
  }
}
```

### POST /moodify
Transform text to match target sentiment.

**Request:**
```json
{
  "text": "I hate this terrible day!",
  "target_sentiment": "positive"
}
```

**Response:**
```json
{
  "original_text": "I hate this terrible day!",
  "modified_text": "I love this wonderful day!",
  "target_sentiment": "positive",
  "original_sentiment": "negative",
  "new_sentiment": "positive",
  "changes_made": ["Transformed from negative to positive sentiment"],
  "success": true,
  "message": "Successfully transformed text to positive!"
}
```

### GET /health
Check service health.

## Models Used

- **Sentiment Analysis**: TextBlob (local)
- **Text Transformation**: DeepSeek Chat v3 (via OpenRouter API)
- **Fallback**: Word replacement system
