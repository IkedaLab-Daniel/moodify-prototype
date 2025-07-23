# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SentimentAnalysisView(APIView):
    def post(self, request):
        user_text = request.data.get("text")
        flask_url = "http://127.0.0.1:5000/predict"

        try:
            flask_response = requests.post(flask_url, json={"text": user_text})
            return Response(flask_response.json(), status=flask_response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class MoodifyTextView(APIView):
    def post(self, request):
        user_text = request.data.get("text")
        target_sentiment = request.data.get("target_sentiment")
        flask_url = "http://localhost:5000/moodify"

        try:
            flask_response = requests.post(flask_url, json={
                "text": user_text, 
                "target_sentiment": target_sentiment
            })
            return Response(flask_response.json(), status=flask_response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)