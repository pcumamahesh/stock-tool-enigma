from django.urls import path
from .views import stock_trends_view, intraday_predictions_view

urlpatterns = [
    path('trends/', stock_trends_view, name='stock_trends'),  # Maps to /api/trends/
    path('intraday/', intraday_predictions_view, name='intraday_predictions'),
]
