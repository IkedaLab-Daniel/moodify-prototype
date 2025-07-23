from django.urls import path
from .views import SentimentAnalysisView, MoodifyTextView

urlpatterns = [
    path('analyze-sentiment/', SentimentAnalysisView.as_view(), name='analyze'),
    path('moodify-text/', MoodifyTextView.as_view(), name='moodify'),
]
