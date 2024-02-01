from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def determine_sentiment(scores):
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment(text):
    if not text:
        return "neutral"
    
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sentiment = determine_sentiment(scores)
    
    return sentiment

def analyze_correlation(sentiment, price_after, price_before):
    if sentiment == "positive" and price_after > price_before:
        return 1
    elif sentiment == "negative" and price_after < price_before:
        return 1
    else:
        return 0