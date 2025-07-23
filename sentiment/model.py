from textblob import TextBlob
import math

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment category
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Calculate confidence based on absolute polarity
    # Higher absolute polarity = higher confidence
    confidence = min(abs(polarity) * 2, 1.0)
    
    # Create detailed scores
    # Normalize polarity (-1 to 1) to positive scores (0 to 1)
    positive_score = max(0, polarity)
    negative_score = max(0, -polarity)
    neutral_score = 1 - abs(polarity)
    
    # Normalize scores so they sum to 1
    total = positive_score + negative_score + neutral_score
    if total > 0:
        positive_score /= total
        negative_score /= total
        neutral_score /= total
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "scores": {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": neutral_score
        }
    }
