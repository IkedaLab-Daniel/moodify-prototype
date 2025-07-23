from textblob import TextBlob
import math
import re

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

def moodify_text(text, target_sentiment):
    """Transform text to match the target sentiment"""
    
    # Define word mappings for sentiment transformation
    positive_words = {
        'bad': 'good', 'terrible': 'wonderful', 'awful': 'amazing', 
        'hate': 'love', 'dislike': 'like', 'horrible': 'fantastic',
        'disappointed': 'pleased', 'frustrated': 'satisfied', 
        'angry': 'happy', 'sad': 'joyful', 'upset': 'delighted',
        'worst': 'best', 'failed': 'succeeded', 'problem': 'opportunity',
        'difficult': 'easy', 'hard': 'simple', 'boring': 'exciting',
        'ugly': 'beautiful', 'stupid': 'smart', 'wrong': 'right'
    }
    
    negative_words = {
        'good': 'bad', 'wonderful': 'terrible', 'amazing': 'awful',
        'love': 'hate', 'like': 'dislike', 'fantastic': 'horrible',
        'pleased': 'disappointed', 'satisfied': 'frustrated',
        'happy': 'angry', 'joyful': 'sad', 'delighted': 'upset',
        'best': 'worst', 'succeeded': 'failed', 'opportunity': 'problem',
        'easy': 'difficult', 'simple': 'hard', 'exciting': 'boring',
        'beautiful': 'ugly', 'smart': 'stupid', 'right': 'wrong'
    }
    
    neutral_words = {
        'love': 'like', 'hate': 'dislike', 'amazing': 'okay',
        'terrible': 'mediocre', 'wonderful': 'decent', 'awful': 'poor',
        'fantastic': 'fine', 'horrible': 'average', 'best': 'okay',
        'worst': 'poor', 'excited': 'interested', 'furious': 'annoyed'
    }
    
    # Sentiment modifiers
    positive_modifiers = ['really', 'very', 'extremely', 'absolutely', 'incredibly']
    negative_modifiers = ['barely', 'hardly', 'somewhat', 'slightly', 'kind of']
    neutral_modifiers = ['quite', 'fairly', 'reasonably', 'moderately']
    
    modified_text = text
    original_sentiment = analyze_sentiment(text)['sentiment']
    
    # If already the target sentiment, return original with note
    if original_sentiment == target_sentiment:
        return {
            "original_text": text,
            "modified_text": text,
            "target_sentiment": target_sentiment,
            "original_sentiment": original_sentiment,
            "changes_made": [],
            "message": f"Text is already {target_sentiment}! No changes needed."
        }
    
    changes_made = []
    
    # Apply word replacements based on target sentiment
    if target_sentiment == "positive":
        word_map = positive_words
        modifier_map = positive_modifiers
    elif target_sentiment == "negative":
        word_map = negative_words  
        modifier_map = negative_modifiers
    else:  # neutral
        word_map = neutral_words
        modifier_map = neutral_modifiers
    
    # Replace words (case-insensitive)
    words = modified_text.split()
    new_words = []
    
    for word in words:
        # Clean word of punctuation for matching
        clean_word = re.sub(r'[^\w]', '', word.lower())
        original_word = word
        
        # Check if word needs replacement
        if clean_word in word_map:
            # Preserve original case and punctuation
            replacement = word_map[clean_word]
            if word[0].isupper():
                replacement = replacement.capitalize()
            
            # Preserve punctuation
            punctuation = re.findall(r'[^\w]', word)
            if punctuation:
                replacement += ''.join(punctuation)
            
            new_words.append(replacement)
            changes_made.append(f"'{original_word}' → '{replacement}'")
        else:
            new_words.append(word)
    
    modified_text = ' '.join(new_words)
    
    # Add sentiment modifiers if needed
    if target_sentiment == "positive" and "very" not in modified_text.lower():
        if "good" in modified_text.lower():
            modified_text = modified_text.replace("good", "really good")
            changes_made.append("Added 'really' for emphasis")
        elif "nice" in modified_text.lower():
            modified_text = modified_text.replace("nice", "really nice")
            changes_made.append("Added 'really' for emphasis")
    
    # Adjust punctuation for sentiment
    if target_sentiment == "positive":
        if modified_text.endswith('.'):
            modified_text = modified_text[:-1] + '!'
            changes_made.append("Changed period to exclamation mark")
    elif target_sentiment == "negative":
        if modified_text.endswith('!'):
            modified_text = modified_text[:-1] + '.'
            changes_made.append("Changed exclamation to period")
    
    # Verify the change worked
    new_sentiment = analyze_sentiment(modified_text)['sentiment']
    
    return {
        "original_text": text,
        "modified_text": modified_text,
        "target_sentiment": target_sentiment,
        "original_sentiment": original_sentiment,
        "new_sentiment": new_sentiment,
        "changes_made": changes_made,
        "success": new_sentiment == target_sentiment,
        "message": f"Successfully transformed text to {target_sentiment}!" if new_sentiment == target_sentiment else f"Attempted transformation, but result is {new_sentiment}"
    }
