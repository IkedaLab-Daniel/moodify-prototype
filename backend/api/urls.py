from django.urls import path
from .views import AnalyzeSentimentView

urlpatterns = [
    path('analyze-sentiment/', AnalyzeSentimentView.as_view(), name='analyze'),
]
