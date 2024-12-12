import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_hi(request):
    data = {
        'message': "Hello, this is a http test",
        'status': 'success'
    }
    
    return Response(data)

@api_view(['POST'])
def post_analysis(request):
    # Access the JSON payload directly
    data = request.data
    return Response({'message': data})