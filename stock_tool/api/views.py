from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Import your utility functions
from .trends_prediction import fetch_data, add_technical_indicators, engineer_features
from .trends_prediction import predict_with_saved_model  # Assuming this is now part of trends_prediction

@csrf_exempt
def stock_trends_view(request):
    if request.method == 'POST':
        try:
            # Parse request body
            body = json.loads(request.body)
            ticker = body.get('ticker', None)
            start_date = body.get('start_date', None)
            end_date = body.get('end_date', None)

            if not ticker or not start_date or not end_date:
                return JsonResponse({"error": "Missing required parameters: ticker, start_date, or end_date"}, status=400)

            # Step 1: Fetch and preprocess stock data
            stock_data = fetch_data(ticker, start_date, end_date)
            stock_data = add_technical_indicators(stock_data)
            stock_data = engineer_features(stock_data)

            # Step 2: Use saved model to make predictions
            prediction = predict_with_saved_model(stock_data)

            return JsonResponse(prediction, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

from .intraday_predictions import (
    fetch_data as fetch_data_intraday, 
    add_technical_indicators as add_tech_indicators_intraday, 
    engineer_features as engg_features_intraday,
    predict_intraday_saved_model
)

@csrf_exempt
def intraday_predictions_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            ticker = body.get('ticker', None)

            if not ticker:
                return JsonResponse({"error": "Ticker is required"}, status=400)

            # Fetch and preprocess stock data
            stock_data = fetch_data_intraday(ticker)
            stock_data = add_tech_indicators_intraday(stock_data)
            stock_data = engg_features_intraday(stock_data)

            # Predict using the saved model
            prediction = predict_intraday_saved_model(stock_data)

            return JsonResponse(prediction, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)