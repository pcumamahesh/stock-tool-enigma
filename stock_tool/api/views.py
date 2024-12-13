# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# # Import your utility functions
# from .trends_prediction import fetch_data, add_technical_indicators, engineer_features
# from .trends_prediction import predict_with_saved_model  # Assuming this is now part of trends_prediction

# @csrf_exempt
# def stock_trends_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse request body
#             body = json.loads(request.body)
#             ticker = body.get('ticker', None)
#             start_date = body.get('start_date', None)
#             end_date = body.get('end_date', None)

#             if not ticker or not start_date or not end_date:
#                 return JsonResponse({"error": "Missing required parameters: ticker, start_date, or end_date"}, status=400)

#             # Step 1: Fetch and preprocess stock data
#             stock_data = fetch_data(ticker, start_date, end_date)
#             stock_data = add_technical_indicators(stock_data)
#             stock_data = engineer_features(stock_data)

#             # Step 2: Use saved model to make predictions
#             prediction = predict_with_saved_model(stock_data)

#             return JsonResponse(prediction, safe=False)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST method is allowed"}, status=405)

# from .intraday_predictions import (
#     fetch_data as fetch_data_intraday, 
#     add_technical_indicators as add_tech_indicators_intraday, 
#     engineer_features as engg_features_intraday,
#     predict_intraday_saved_model
# )

# @csrf_exempt
# def intraday_predictions_view(request):
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             ticker = body.get('ticker', None)

#             if not ticker:
#                 return JsonResponse({"error": "Ticker is required"}, status=400)

#             # Fetch and preprocess stock data
#             stock_data = fetch_data_intraday(ticker)
#             stock_data = add_tech_indicators_intraday(stock_data)
#             stock_data = engg_features_intraday(stock_data)

#             # Predict using the saved model
#             prediction = predict_intraday_saved_model(stock_data)

#             return JsonResponse(prediction, safe=False)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST method is allowed"}, status=405)

# !<-------------------------------------------Updated Code------------------------------------------------------------->

from django.http import JsonResponse
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
        # Get the query parameters
        ticker = request.GET.get('ticker', 'RELIANCE.NS')  # Default ticker if not provided
        start_date = request.GET.get('start_date', '2020-01-01')  # Default start date
        end_date = request.GET.get('end_date', '2023-12-01')  # Default end date

        # Parse dates (ensure proper format)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Fetch historical stock data from Yahoo Finance
        stock_data = fetch_data(ticker, start_date, end_date)
        
        # Add technical indicators like RSI and MACD
        stock_data = add_technical_indicators(stock_data)

        # Feature Engineering
        stock_data = engineer_features(stock_data)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = split_data(stock_data)

        # Train the model
        model, mae = train_model(X_train, y_train, X_test, y_test)

        # Get the prediction
        prediction = predict_trend_and_price(model, stock_data)

        # Return prediction results as JSON
        return JsonResponse(prediction)

# Endpoint for predicting intraday trend
@csrf_exempt
def intraday_predictions_view(request):
    if request.method == 'GET':
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

        # Return prediction results as JSON
        return JsonResponse(prediction)
