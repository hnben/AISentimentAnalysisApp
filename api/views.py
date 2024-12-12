from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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

@api_view(['GET'])
def get_analysis(request):
    # Retrieve all records from the SentimentAnalysis model
    sentiment_analyses = SentimentAnalysis.objects.all()

    # Prepare a list of dictionaries to send in the response
    analysis_data = []
    for analysis in sentiment_analyses:
        analysis_data.append({
            'name': analysis.name,
            'message': analysis.message,
            'analysis': analysis.analysis
        })

    # Return the data as a JSON response
    return Response(analysis_data, status=status.HTTP_200_OK)



@api_view(['POST'])
def post_analysis(request):
    # Extract the message and name from the incoming request
    data = request.data
    message = data.get('message', '')
    name = data.get('name', 'Unknown')  # Default to 'Unknown' if no name is provided

    if not message:
        return Response({'error': 'Message not provided'}, status=400)

    # First, check if the result is in the cache
    cached_result = cache.get(message)

    if cached_result:
        # If the result is cached, return it
        return Response({
            'name': name,
            'analysis_result': cached_result
        })

    # Check if the result is already in the database
    existing_result = SentimentAnalysis.objects.filter(message=message).first()

    if existing_result:
        # If it's in the database, return the cached result
        cache.set(message, existing_result.analysis, timeout=60*15)  # Cache timeout for 15 minutes
        return Response({
            'name': existing_result.name,
            'analysis_result': existing_result.analysis
        })

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
    sentiment_analysis = SentimentAnalysis.objects.create(
        name=name, 
        message=message, 
        analysis=analysis_result
    )

    # Cache the result for future requests
    cache.set(message, analysis_result, timeout=60*15)  # Cache timeout for 15 minutes

    # Return both name and analysis result in the response
    return Response({
        'name': sentiment_analysis.name,
        'analysis_result': analysis_result
    })