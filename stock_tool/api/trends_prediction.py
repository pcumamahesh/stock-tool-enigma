# import yfinance as yf
# import requests
# from ta.momentum import RSIIndicator
# from ta.trend import MACD
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error
# from bs4 import BeautifulSoup
# import joblib
# import numpy as np

# # Step 1: Fetch historical stock data from Yahoo Finance (Primary)
# def fetch_data(ticker, start_date, end_date):
#     stock_data = yf.download(ticker, start=start_date, end=end_date)
#     stock_data = stock_data[['Close']].dropna()  # Use only closing prices
#     return stock_data

# # Step 2: Optionally Fetch Data from NSE/BSE using Web Scraping (Alternative Data Source)
# def fetch_nse_data(stock_symbol):
#     url = f'https://www.nseindia.com/get-quotes/equity?symbol={stock_symbol}'
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Extract relevant data (example: stock price or other metrics)
#     # You need to inspect the webpage for extracting the correct data point
#     return soup  # Modify this to extract the stock data you need

# # Step 3: Add Technical Indicators (RSI and MACD)
# def add_technical_indicators(stock_data):
#     close_prices = stock_data['Close'].squeeze()  # Ensure it's a 1D Series

#     # RSI (Relative Strength Index)
#     rsi = RSIIndicator(close_prices)
#     stock_data['RSI'] = rsi.rsi()

#     # MACD (Moving Average Convergence Divergence)
#     macd = MACD(close_prices)
#     stock_data['MACD'] = macd.macd()
#     stock_data['Signal_Line'] = macd.macd_signal()

#     return stock_data

# # Step 4: Feature Engineering (Add Lagged Features)
# def engineer_features(stock_data):
#     stock_data['Close_Lag1'] = stock_data['Close'].shift(1)
#     stock_data['Close_Lag2'] = stock_data['Close'].shift(2)
#     stock_data.dropna(inplace=True)  # Drop rows with NaN values
#     return stock_data

# # Step 5: Split Data into Training and Test Sets
# def split_data(stock_data):
#     X = stock_data[['Close_Lag1', 'Close_Lag2', 'RSI', 'MACD']]
#     y = stock_data['Close']
    
#     # Temporal split: 80% for training, 20% for testing
#     train_size = int(len(stock_data) * 0.8)
#     X_train, X_test = X[:train_size], X[train_size:]
#     y_train, y_test = y[:train_size], y[train_size:]
    
#     return X_train, X_test, y_train, y_test

# # Step 6: Train the Random Forest Model
# def train_model(X_train, y_train, X_test, y_test):
#     model = RandomForestRegressor(n_estimators=600, max_depth=30, random_state=42)
#     model.fit(X_train, y_train.values.ravel())
    
#     # Make predictions
#     y_pred = model.predict(X_test)
    
#     # Calculate MAE (Mean Absolute Error)
#     mae = mean_absolute_error(y_test, y_pred)
#     print(f"Model Trained - MAE: {mae}")
    
#     return model, mae

# # Step 7: Predict Trend and Closing Price for the Next Day
# def predict_trend_and_price(model, stock_data):
#     # Predict next day's closing price (using the last available data)
#     last_row = stock_data.iloc[-1]
    
#     # Ensure it's a 2D array with shape (1, number_of_features)
#     last_features = np.array([[
#         last_row['Close_Lag1'], 
#         last_row['Close_Lag2'], 
#         last_row['RSI'], 
#         last_row['MACD']
#     ]])

#     # Reshaping to ensure it's 2D (1, 4)
#     last_features = last_features.reshape(1, -1)

#     # Make the prediction for the next day's closing price
#     predicted_price = model.predict(last_features)[0]
    
#     # Ensure last_price is a scalar (using .item() or .iloc[0])
#     last_price = last_row['Close'].item()  # Or .iloc[0] if it's a DataFrame

#     # Classify the trend
#     if predicted_price > last_price:
#         trend = "Uptrend"
#         confidence = (predicted_price - last_price) / predicted_price * 100  # Confidence as % increase
#     elif predicted_price < last_price:
#         trend = "Downtrend"
#         confidence = (last_price - predicted_price) / last_price * 100  # Confidence as % decrease
#     else:
#         trend = "Neutral"
#         confidence = 0  # No change
    
#     # Return the output in a structured format (JSON-like)
#     output = {
#         "ticker": stock_data.index[-1],  # Date of the last entry (next prediction)
#         "predicted_close": round(predicted_price, 2),
#         "predicted_trend": trend,
#         "confidence": round(confidence, 2)
#     }
    
#     return output

# # Step 8: Save the Model (for later use in deployment)
# def save_model(model, filename='stock_trend_model.pkl'):
#     joblib.dump(model, filename)
#     print(f"Model saved as {filename}")

# import os
# from django.conf import settings

# def load_model(filename='stock_trend_model.pkl'):
#     # Get the absolute path to the .pkl file in the same directory as the script
#     model_file_path = os.path.join(settings.BASE_DIR, "api", filename)
    
#     if not os.path.exists(model_file_path):
#         raise FileNotFoundError(f"Model file not found at: {model_file_path}")
    
#     model = joblib.load(model_file_path)
#     return model

# def predict_with_saved_model(stock_data, model_filename='stock_trend_model.pkl'):
#     # Load the saved model
#     model = load_model(model_filename)

#     # Extract the last row of stock data for prediction
#     last_row = stock_data.iloc[-1]
#     last_features = np.array([[  # Match the model's input features
#         last_row['Close_Lag1'], 
#         last_row['Close_Lag2'], 
#         last_row['RSI'], 
#         last_row['MACD']
#     ]]).reshape(1, -1)  # Ensure it's 2D (1 sample, N features)

#     # Predict next day's closing price
#     predicted_price = model.predict(last_features)[0]

#     # Get the last closing price
#     last_price = last_row['Close'].item()

#     # Determine trend and confidence
#     if predicted_price > last_price:
#         trend = "Uptrend"
#         confidence = (predicted_price - last_price) / predicted_price * 100
#     elif predicted_price < last_price:
#         trend = "Downtrend"
#         confidence = (last_price - predicted_price) / last_price * 100
#     else:
#         trend = "Neutral"
#         confidence = 0

    # return {
#         "ticker": stock_data.index[-1],  # Date of prediction
#         "predicted_close": round(predicted_price, 2),
#         "predicted_trend": trend,
#         "confidence": round(confidence, 2)
#     }

# # # Main Function to Execute All Steps
# # def main():
# #     ticker = "RELIANCE.NS"  # Example ticker for NSE
# #     start_date = "2020-01-01"
# #     end_date = "2023-12-01"
    
# #     # Step 1: Fetch Data (Using Yahoo Finance)
# #     stock_data = fetch_data(ticker, start_date, end_date)
    
# #     # Step 2: Optionally fetch data from NSE/BSE
# #     fetch_nse_data('RELIANCE')  # Can be used for scraping additional data
    
# #     # Step 3: Add Technical Indicators
# #     stock_data = add_technical_indicators(stock_data)
    
# #     # Step 4: Feature Engineering
# #     stock_data = engineer_features(stock_data)
    
# #     # Step 5: Split Data
# #     X_train, X_test, y_train, y_test = split_data(stock_data)
    
# #     # Step 6: Train Model
# #     model, mae = train_model(X_train, y_train, X_test, y_test)
    
# #     # Step 7: Predict Trend and Price
# #     prediction = predict_trend_and_price(model, stock_data)
    
# #     # Output the results in JSON-like format (for use in UI/Backend)
# #     print(prediction)
    
# #     # Step 8: Save the Model
# #     save_model(model)

# def main(ticker="RELIANCE.NS", start_date="2020-01-01", end_date="2023-12-01"):
#     """
#     Main function to fetch data, train model, and make predictions.

#     Args:
#     - ticker (str): Stock ticker symbol (e.g., "RELIANCE.NS").
#     - start_date (str): Start date for historical data (format: "YYYY-MM-DD").
#     - end_date (str): End date for historical data (format: "YYYY-MM-DD").

#     Returns:
#     - dict: Prediction results including predicted close price, trend, and confidence.
#     """
#     try:
#         # Step 1: Fetch Data
#         stock_data = fetch_data(ticker, start_date, end_date)

#         # Step 2: Optionally fetch data from NSE/BSE
#         fetch_nse_data(ticker)  # For additional data, if required

#         # Step 3: Add Technical Indicators
#         stock_data = add_technical_indicators(stock_data)

#         # Step 4: Feature Engineering
#         stock_data = engineer_features(stock_data)

#         # Step 5: Split Data
#         X_train, X_test, y_train, y_test = split_data(stock_data)

#         # Step 6: Train Model
#         model, mae = train_model(X_train, y_train, X_test, y_test)

#         # Step 7: Predict Trend and Price
#         prediction = predict_trend_and_price(model, stock_data)

#         # Return prediction for the API
#         return prediction

#     except Exception as e:
#         return {"error": str(e)}


# # Run the main function
# if __name__ == "__main__":
#     main()

# <!--------------------------------------------Updated code---------------------------------------------------->

# trends_prediction.py
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np

def fetch_data(ticker, start_date, end_date):
    # Fetch historical data from Yahoo Finance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data[['Close']].dropna()  # Use only closing prices
    return stock_data

def add_technical_indicators(stock_data):
    close_prices = stock_data['Close'].squeeze()

    # RSI (Relative Strength Index)
    rsi = RSIIndicator(close_prices)
    stock_data['RSI'] = rsi.rsi()

    # MACD (Moving Average Convergence Divergence)
    macd = MACD(close_prices)
    stock_data['MACD'] = macd.macd()
    stock_data['Signal_Line'] = macd.macd_signal()

    return stock_data

def engineer_features(stock_data):
    stock_data['Close_Lag1'] = stock_data['Close'].shift(1)
    stock_data['Close_Lag2'] = stock_data['Close'].shift(2)
    stock_data.dropna(inplace=True)
    return stock_data

def split_data(stock_data):
    X = stock_data[['Close_Lag1', 'Close_Lag2', 'RSI', 'MACD']]
    y = stock_data['Close']
    
    # Temporal split: 80% for training, 20% for testing
    train_size = int(len(stock_data) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, X_test, y_test):
    model = RandomForestRegressor(n_estimators=600, max_depth=30, random_state=42)
    model.fit(X_train, y_train.values.ravel())
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate MAE (Mean Absolute Error)
    mae = mean_absolute_error(y_test, y_pred)
    return model, mae

def predict_trend_and_price(model, stock_data):
    last_row = stock_data.iloc[-1]
    
    last_features = np.array([[last_row['Close_Lag1'], last_row['Close_Lag2'], last_row['RSI'], last_row['MACD']]])
    last_features = last_features.reshape(1, -1)

    predicted_price = model.predict(last_features)[0]
    last_price = last_row['Close'].item()

    if predicted_price > last_price:
        trend = "Uptrend"
        confidence = (predicted_price - last_price) / predicted_price * 100
    elif predicted_price < last_price:
        trend = "Downtrend"
        confidence = (last_price - predicted_price) / last_price * 100
    else:
        trend = "Neutral"
        confidence = 0
    
    output = {
        "ticker": stock_data.index[-1],
        "predicted_close": round(predicted_price, 2),
        "predicted_trend": trend,
        "confidence": round(confidence, 2)
    }
    
    return output
