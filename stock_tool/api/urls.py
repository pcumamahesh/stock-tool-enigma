from django.urls import path
from .views import stock_trends_view

urlpatterns = [
    path('trends/', stock_trends_view, name='stock_trends'),  # Maps to /api/trends/
]
