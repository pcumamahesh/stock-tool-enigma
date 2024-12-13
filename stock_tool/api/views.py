from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .trends_prediction import (
    fetch_data, 
    add_technical_indicators, 
    engineer_features, 
    split_data, 
    train_model, 
    predict_trend_and_price
)
from .intraday_predictions import (
    fetch_data as fetch_intraday_data, 
    add_technical_indicators as add_intraday_technical_indicators, 
    engineer_features as engineer_intraday_features, 
    split_data as split_intraday_data, 
    train_model as train_intraday_model, 
    predict_intraday_trend_and_price
)

# Endpoint for predicting stock trend
@csrf_exempt
def stock_trends_view(request):
    if request.method == 'GET':
        try:
            # Get the query parameters
            ticker = request.GET.get('ticker', 'RELIANCE.NS')
            start_date = request.GET.get('start_date', '2020-01-01')
            end_date = request.GET.get('end_date', '2023-12-01')

            # Parse dates
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if not start_date or not end_date:
                return render(request, 'error.html', {"error": "Invalid date format. Use YYYY-MM-DD."})

            # Fetch historical stock data
            stock_data = fetch_data(ticker, start_date, end_date)
            stock_data = add_technical_indicators(stock_data)
            stock_data = engineer_features(stock_data)

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = split_data(stock_data)

            # Train the model
            model, mae = train_model(X_train, y_train, X_test, y_test)

            # Get the prediction
            prediction = predict_trend_and_price(model, stock_data)

            return render(request, 'stock_trends.html', {'prediction': prediction})
        except Exception as e:
            return render(request, 'error.html', {"error": f"Internal server error: {str(e)}"})

    return render(request, 'error.html', {"error": "Only GET method is allowed"})

# Endpoint for predicting intraday trend
@csrf_exempt
def intraday_predictions_view(request):
    if request.method == 'GET':
        try:
            # Get the query parameters
            ticker = request.GET.get('ticker', 'RELIANCE.NS')  # Default ticker if not provided

            # Fetch intraday stock data (1-minute interval)
            stock_data = fetch_intraday_data(ticker)

            # Add technical indicators like RSI and MACD
            stock_data = add_intraday_technical_indicators(stock_data)

            # Feature Engineering
            stock_data = engineer_intraday_features(stock_data)

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = split_intraday_data(stock_data)

            # Train the model
            model, mae = train_intraday_model(X_train, y_train, X_test, y_test)

            # Get the intraday prediction
            prediction = predict_intraday_trend_and_price(model, stock_data)

            # Render the prediction results in an HTML template
            return render(request, 'intraday_predictions.html', {'prediction': prediction})
        except Exception as e:
            return render(request, 'error.html', {"error": f"Internal server error: {str(e)}"})

    return render(request, 'error.html', {"error": "Only GET method is allowed"})
