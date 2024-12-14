# from django.urls import path
# from .views import stock_trends_view, intraday_predictions_view

# urlpatterns = [
#     path('trends/', stock_trends_view, name='stock_trends'),  # Maps to /api/trends/
#     path('intraday/', intraday_predictions_view, name='intraday_predictions'),
# ]

# <!----------------------------Updated Code------------------------------------------->
# from django.urls import path
# from .views import stock_trends_view, intraday_predictions_view, main_page_view

# urlpatterns = [
#     path('', main_page_view, name='main_page'),  # Main page
#     path('trends/', stock_trends_view, name='stock_trends'),  # Maps to /api/trends/
#     path('intraday/', intraday_predictions_view, name='intraday_predictions'),  # Maps to /api/intraday/
# ]

from django.urls import path
from .views import home_page_view, intraday_predictions_view, stock_trends_view, suggest_view

urlpatterns = [
    path('', home_page_view, name='home'),  # Root view
    path('intraday/', intraday_predictions_view, name='intraday'),  # Intraday predictions
    path('stock_trends/', stock_trends_view, name='stock_trends'),  # Stock trends
    path('suggest/', suggest_view, name='suggest'),
]
