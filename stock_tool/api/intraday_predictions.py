import yfinance as yf
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import time
from datetime import datetime

# Step 1: Fetch historical stock data from Yahoo Finance (Primary)
def fetch_data(ticker):
    # Use the current date as the end_date
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    stock_data = yf.download(ticker, period="1d", interval="1m")
    stock_data = stock_data[['Close']].dropna()  # Use only closing prices
    return stock_data

# Step 2: Add Technical Indicators (RSI and MACD)
def add_technical_indicators(stock_data):
    close_prices = stock_data['Close'].squeeze()  # Ensure it's a 1D Series

    # RSI (Relative Strength Index)
    rsi = RSIIndicator(close_prices)
    stock_data['RSI'] = rsi.rsi()

    # MACD (Moving Average Convergence Divergence)
    macd = MACD(close_prices)
    stock_data['MACD'] = macd.macd()
    stock_data['Signal_Line'] = macd.macd_signal()

    return stock_data

# Step 3: Feature Engineering (Add Lagged Features)
def engineer_features(stock_data):
    stock_data['Close_Lag1'] = stock_data['Close'].shift(1)
    stock_data['Close_Lag2'] = stock_data['Close'].shift(2)
    stock_data.dropna(inplace=True)  # Drop rows with NaN values
    return stock_data

# Step 4: Split Data into Training and Test Sets
def split_data(stock_data):
    X = stock_data[['Close_Lag1', 'Close_Lag2', 'RSI', 'MACD']]
    y = stock_data['Close']
    
    # Temporal split: 80% for training, 20% for testing
    train_size = int(len(stock_data) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    return X_train, X_test, y_train, y_test

# Step 5: Train the Random Forest Model
def train_model(X_train, y_train, X_test, y_test):
    model = RandomForestRegressor(n_estimators=600, max_depth=30, random_state=42)
    model.fit(X_train, y_train.values.ravel())
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate MAE (Mean Absolute Error)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model Trained - MAE: {mae}")
    
    return model, mae

# Step 6: Predict Intraday Trend and Closing Price for Today
def predict_intraday_trend_and_price(model, stock_data):
    # Predict today's closing price based on the last available data
    last_row = stock_data.iloc[-1]
    
    # Ensure it's a 2D array with shape (1, number_of_features)
    last_features = np.array([[last_row['Close_Lag1'], last_row['Close_Lag2'], last_row['RSI'], last_row['MACD']]])

    # Reshaping to ensure it's 2D (1, 4)
    last_features = last_features.reshape(1, -1)

    # Make the prediction for today's closing price
    predicted_price = model.predict(last_features)[0]
    
    # Ensure last_price is a scalar (using .item() or .iloc[0])
    last_price = last_row['Close'].item()  # Or .iloc[0] if it's a DataFrame

    # Classify the trend
    if predicted_price > last_price:
        trend = "Uptrend"
        confidence = (predicted_price - last_price) / predicted_price * 100  # Confidence as % increase
    elif predicted_price < last_price:
        trend = "Downtrend"
        confidence = (last_price - predicted_price) / last_price * 100  # Confidence as % decrease
    else:
        trend = "Neutral"
        confidence = 0  # No change
    
    # Return the output in a structured format (JSON-like)
    output = {
        "predicted_close": round(predicted_price, 2),
        "predicted_trend": trend,
        "confidence": round(confidence, 2)
    }
    
    return output

# Step 7: Save the Model (for later use in deployment)
def save_model(model, filename='intraday_trend.pkl'):
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

import os
from django.conf import settings

def predict_intraday_saved_model(stock_data, model_path="intraday_trend.pkl"):
    model_file_path = os.path.join(settings.BASE_DIR, "api", model_path)
    
    if not os.path.exists(model_file_path):
        raise FileNotFoundError(f"Model file not found at: {model_file_path}")
    
    # load the saved intraday model
    model = joblib.load(model_file_path)

    # Extract the last row for prediction
    last_row = stock_data.iloc[-1]
    last_features = np.array([[last_row['Close_Lag1'], last_row['Close_Lag2'], last_row['RSI'], last_row['MACD']]])
    last_features = last_features.reshape(1, -1)

    # Predict the price
    predicted_price = model.predict(last_features)[0]
    last_price = last_row['Close'].item()

    # Determine trend and confidence
    if predicted_price > last_price:
        trend = "Uptrend"
        confidence = (predicted_price - last_price) / predicted_price * 100
    elif predicted_price < last_price:
        trend = "Downtrend"
        confidence = (last_price - predicted_price) / last_price * 100
    else:
        trend = "Neutral"
        confidence = 0

    return {
        "predicted_close": round(predicted_price, 2),
        "predicted_trend": trend,
        "confidence": round(confidence, 2)
    }

# Main Function to Execute All Steps
def main():
    ticker = "HDFCBANK.NS"  # Example ticker for NSE
    
    # Step 1: Fetch Data (Using Yahoo Finance) for intraday (real-time)
    stock_data = fetch_data(ticker)
    
    # Step 2: Add Technical Indicators
    stock_data = add_technical_indicators(stock_data)
    
    # Step 3: Feature Engineering
    stock_data = engineer_features(stock_data)
    
    # Step 4: Split Data
    X_train, X_test, y_train, y_test = split_data(stock_data)
    
    # Step 5: Train Model
    model, mae = train_model(X_train, y_train, X_test, y_test)
    save_model(model=model)
    
    # Step 6: Continuously Fetch New Data and Predict Intraday Trend and Price
    while True:
        # Fetch updated stock data for the day
        stock_data = fetch_data(ticker)
        stock_data = add_technical_indicators(stock_data)
        stock_data = engineer_features(stock_data)
        
        # Predict Intraday Trend and Price
        prediction = predict_intraday_trend_and_price(model, stock_data)
        
        # Output the results for intraday prediction
        print(f"Predicted Closing Price for Today: ₹{prediction['predicted_close']}")
        print(f"Predicted Trend: {prediction['predicted_trend']}")
        print(f"Confidence: {prediction['confidence']}%")
        
        # Wait for 1 minute before fetching the new data (or adjust as needed)
        time.sleep(60)  # Adjust the sleep time based on how frequently you want updates

# Run the main function
if __name__ == "__main__":
    main()
