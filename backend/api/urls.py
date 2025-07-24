from django.urls import path
from .views import (
    SentimentAnalysisView, 
    MoodifyTextView,
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Sentiment analysis endpoints
    path('analyze-sentiment/', SentimentAnalysisView.as_view(), name='analyze'),
    path('moodify-text/', MoodifyTextView.as_view(), name='moodify'),
]
