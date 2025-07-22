import requests
import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeSentimentView(View):
    def post(self, request):
        data = json.loads(request.body)
        text = data.get('text')
        resp = requests.post('http://sentiment:5000/analyze', json={'text': text})
        return JsonResponse(resp.json())
