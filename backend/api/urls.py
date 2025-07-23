from django.urls import path
from .views import SentimentAnalysisView

urlpatterns = [
    path('analyze-sentiment/', SentimentAnalysisView.as_view(), name='analyze'),
]
