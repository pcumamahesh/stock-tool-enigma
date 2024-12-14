import tweepy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Replace with your own Twitter API credentials
API_KEY = "NAz6DkUbNYmg7qCLKeheS6EOC"
API_SECRET_KEY = "DaeSCud8E9Z2EyRE7uwJXiOkaUoDyD8mkjAIiIHNvHGCAKB2Cv"
ACCESS_TOKEN = "1671692880551845894-IGgBhF2Bw8vLHabxzh2lTbSejSod9o"
ACCESS_TOKEN_SECRET = "B8WZogVAxV81GwF6XhmpJv9gePNBPhGIiaA1sjd9vGZlt"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIYkxgEAAAAA8IcdHWeVM58Hj0TYIyE7HmWmbDM%3DY5AC85TxQsTPwAj30vAwrWUNClxX2tBdoUqFSTIVCJppPCOTvJ"

# Initialize Tweepy Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch tweets related to a stock
def fetch_stock_tweets(stock_symbol, max_results=100):
    query = f"{stock_symbol} lang:en -is:retweet"  # Search tweets mentioning the stock symbol, exclude retweets
    try:
        response = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text"], max_results=max_results)
        if response.data:
            tweets_data = [(tweet.text, tweet.created_at) for tweet in response.data]
            return pd.DataFrame(tweets_data, columns=["Tweet", "CreatedAt"])
        else:
            print("No tweets found for this stock symbol.")
            return pd.DataFrame(columns=["Tweet", "CreatedAt"])
    except Exception as e:
        print("Error fetching tweets:", e)
        return pd.DataFrame(columns=["Tweet", "CreatedAt"])

# Function to analyze sentiment of tweets
def analyze_sentiment(dataframe):
    sentiments = []
    sentiment_ratings = []
    for tweet in dataframe["Tweet"]:
        sentiment_score = analyzer.polarity_scores(tweet)
        compound_score = sentiment_score["compound"]

        # Map compound score to 1-100 scale
        if compound_score <= -0.5:
            sentiment_rating = (compound_score + 1) * 20  # Negative Sentiment (1-40)
        elif compound_score <= 0.5:
            sentiment_rating = (compound_score * 40) + 50  # Neutral Sentiment (41-60)
        else:
            sentiment_rating = (compound_score * 50) + 50  # Positive Sentiment (61-100)

        # Categorize sentiment
        if sentiment_rating <= 40:
            sentiment_category = "Strong Sell"
        elif sentiment_rating <= 60:
            sentiment_category = "Neutral"
        else:
            sentiment_category = "Strong Buy"

        sentiments.append(sentiment_category)
        sentiment_ratings.append(sentiment_rating)

    dataframe["SentimentScore"] = sentiment_ratings
    dataframe["Sentiment"] = sentiments
    return dataframe

# Example Usage
stock_symbol = "RELIANCE"  # Replace with the desired stock symbol (e.g., AAPL, TSLA)

# Fetch tweets related to the stock
tweets_df = fetch_stock_tweets(stock_symbol)

if not tweets_df.empty:
    # Analyze sentiment of the tweets
    analyzed_df = analyze_sentiment(tweets_df)

    # Display results
    print("\nSentiment Analysis Results:")
    print(analyzed_df)

    # Calculate overall sentiment trend
    sentiment_trend = analyzed_df["Sentiment"].value_counts()
    print("\nSentiment Trend:")
    print(sentiment_trend)
else:
    print("No tweets data available for sentiment analysis.")