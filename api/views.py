from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SentimentAnalysis
from django.core.cache import cache

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
    # Extract the message from the incoming request
    data = request.data
    message = data.get('message', '')

    if not message:
        return Response({'error': 'Message not provided'}, status=400)

    # First, check if the result is in the cache
    cached_result = cache.get(message)

    if cached_result:
        # If the result is cached, return it
        return Response(cached_result)

    # Check if the result is already in the database
    existing_result = SentimentAnalysis.objects.filter(message=message).first()

    if existing_result:
        # If it's in the database, return the cached result
        cache.set(message, existing_result.analysis_result, timeout=60*15)  # Cache timeout for 15 minutes
        return Response(existing_result.analysis_result)

    # If the message is not found in cache or database, perform sentiment analysis
    tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
    model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Perform aspect-based sentiment analysis for the given message
    analysis_result = {
        'food': classifier(message, text_pair='food'),
        'service': classifier(message, text_pair='service'),
        'atmosphere': classifier(message, text_pair='atmosphere'),
        'cost': classifier(message, text_pair='cost'),
    }

    # Store the result in the database
    SentimentAnalysis.objects.create(message=message, analysis_result=analysis_result)

    # Cache the result for future requests
    cache.set(message, analysis_result, timeout=60*15)  # Cache timeout for 15 minutes

    return Response(analysis_result)