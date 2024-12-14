# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.dateparse import parse_date
# from .trends_prediction import (
#     fetch_data, 
#     add_technical_indicators, 
#     engineer_features, 
#     split_data, 
#     train_model, 
#     predict_trend_and_price
# )
# from .intraday_predictions import (
#     fetch_data as fetch_intraday_data, 
#     add_technical_indicators as add_intraday_technical_indicators, 
#     engineer_features as engineer_intraday_features, 
#     split_data as split_intraday_data, 
#     train_model as train_intraday_model, 
#     predict_intraday_trend_and_price
# )

# # Endpoint for predicting stock trend
# @csrf_exempt
# def stock_trends_view(request):
#     if request.method == 'GET':
#         try:
#             # Get the query parameters
#             ticker = request.GET.get('ticker', 'RELIANCE.NS')
#             start_date = request.GET.get('start_date', '2020-01-01')
#             end_date = request.GET.get('end_date', '2023-12-01')

#             # Parse dates
#             start_date = parse_date(start_date)
#             end_date = parse_date(end_date)

#             if not start_date or not end_date:
#                 return render(request, 'error.html', {"error": "Invalid date format. Use YYYY-MM-DD."})

#             # Fetch historical stock data
#             stock_data = fetch_data(ticker, start_date, end_date)
#             stock_data = add_technical_indicators(stock_data)
#             stock_data = engineer_features(stock_data)

#             # Split the data into training and testing sets
#             X_train, X_test, y_train, y_test = split_data(stock_data)

#             # Train the model
#             model, mae = train_model(X_train, y_train, X_test, y_test)

#             # Get the prediction
#             prediction = predict_trend_and_price(model, stock_data)

#             return render(request, 'stock_trends.html', {'prediction': prediction})
#         except Exception as e:
#             return render(request, 'error.html', {"error": f"Internal server error: {str(e)}"})

#     return render(request, 'error.html', {"error": "Only GET method is allowed"})

# # Endpoint for predicting intraday trend
# @csrf_exempt
# def intraday_predictions_view(request):
#     if request.method == 'GET':
#         try:
#             # Get the query parameters
#             ticker = request.GET.get('ticker', 'HDFCBANK.NS')  # Default ticker if not provided

#             # Fetch intraday stock data (1-minute interval)
#             stock_data = fetch_intraday_data(ticker)

#             # Add technical indicators like RSI and MACD
#             stock_data = add_intraday_technical_indicators(stock_data)

#             # Feature Engineering
#             stock_data = engineer_intraday_features(stock_data)

#             # Split the data into training and testing sets
#             X_train, X_test, y_train, y_test = split_intraday_data(stock_data)

#             # Train the model
#             model, mae = train_intraday_model(X_train, y_train, X_test, y_test)

#             # Get the intraday prediction
#             prediction = predict_intraday_trend_and_price(model, stock_data)

#             # Render the prediction results in an HTML template
#             return render(request, 'intraday_predictions.html', {'prediction': prediction})
#         except Exception as e:
#             return render(request, 'error.html', {"error": f"Internal server error: {str(e)}"})

#     return render(request, 'error.html', {"error": "Only GET method is allowed"})

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .intraday_predictions import (
    fetch_data as fetch_intraday_data,
    add_technical_indicators as add_intraday_technical_indicators,
    engineer_features as engineer_intraday_features,
    split_data as split_intraday_data,
    train_model as train_intraday_model,
    predict_intraday_trend_and_price
)

@csrf_exempt
def intraday_predictions_view(request):
    if request.method == 'POST':
        try:
            # Retrieve ticker from the form input
            ticker = request.POST.get('ticker', 'HDFCBANK.NS')  # Default ticker if not provided

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

            # Extract necessary fields
            trend = prediction.get("predicted_trend", "No trend available")
            confidence = prediction.get("confidence", "No confidence available")
            returns = prediction.get("predicted_close", "No value available")

            # Render the template with results
            return render(
                request,
                'intraday_combined.html',
                {'trend': trend, 'confidence': confidence, 'returns': returns, 'ticker': ticker}
            )
        except Exception as e:
            return render(request, 'intraday_combined.html', {"error": f"Internal server error: {str(e)}"})

    # Render empty form for GET request
    return render(request, 'intraday_combined.html')

from django.shortcuts import render
from django.utils.dateparse import parse_date
from .trends_prediction import fetch_data, add_technical_indicators, engineer_features, split_data, train_model, predict_trend_and_price

@csrf_exempt
def stock_trends_view(request):
    if request.method == 'POST':
        try:
            # Retrieve ticker and dates from the form input
            ticker = request.POST.get('ticker', 'RELIANCE.NS')  # Default ticker if not provided
            start_date = request.POST.get('start_date', '2020-01-01')
            end_date = request.POST.get('end_date', '2023-12-01')

            # Parse dates
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if not start_date or not end_date:
                return render(request, 'stock_trends_combined.html', {"error": "Invalid date format. Use YYYY-MM-DD."})

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

            # Extract necessary fields
            trend = prediction.get("predicted_trend", "No trend available")
            confidence = prediction.get("confidence", "No confidence available")
            returns = prediction.get("predicted_close", "No value available")

            # Render the template with results
            return render(
                request,
                'stock_trends_combined.html',
                {'trend': trend, 'confidence': confidence, 'returns': returns, 'ticker': ticker}
            )
        except Exception as e:
            return render(request, 'stock_trends_combined.html', {"error": f"Internal server error: {str(e)}"})

    # Render empty form for GET request
    return render(request, 'stock_trends_combined.html')

def home_page_view(request):
    """
    Root view to display links to Intraday Predictions, Stock Trends, and Sentiment Analysis.
    """
    return render(request, 'home_page.html')

import os
import google.generativeai as genai

genai.configure(api_key='AIzaSyBEv2Y_SlCODfYWstJd8013k5Zn8UAgdZ8')

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="you are a stock suggesting assistant that will suggest stocks on the bases of our prediction models allong with current sentimental analysis you should be consise and give pointes on why some stock needs to be selected all the merits and demerits some time you will be provided with inputs about some stock highed priority should be given to that reason the ned goal for you is to provide suggestion and accurate reasoning  , you should only suggest indian stock ,i .e stock available in NSE and BSE also at most you should suggest 2 stocks and 4 reasons no more conversation only preciese points do not explicitly mention indian.",
)

def suggest_view(request):
    response_text = ""
    if request.method == 'POST':
        user_input = request.POST.get('stock_input', '')
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        user_input,
                    ],
                },
            ]
        )
        response = chat_session.send_message(user_input)
        response_text = response.text.split('.')

    return render(request, 'suggest.html', {'response_text': response_text})