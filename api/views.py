import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

#model imports
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

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
    message = data.get("review", "")
    
    #throw error if not the right format or string
    if not isinstance(message, str):
        return Response({'error': 'Invalid message format'}, status=400)
    
    
    tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
    model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
    
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Prepare the result dictionary
    aspect_results = {}

    # Perform aspect-based sentiment analysis for each aspect
    for aspect in ['food', 'service', 'atmosphere', 'cost']:
        # Use the classifier on the message with the specific aspect as text_pair
        result = classifier(message, text_pair=aspect)
        aspect_results[aspect] = result

    # Return the results as a JSON response
    return Response({'analysis': aspect_results})

