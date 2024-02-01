from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def determine_sentiment(scores):
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"