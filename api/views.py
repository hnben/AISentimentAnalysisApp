import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SentimentAnalysis
from django.core.cache import cache

#model imports
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
from groq import Groq

@api_view(['GET'])
def get_hi(request):
    data = {
        'message': "Hello, this is a http test",
        'status': 'success'
    }
    return Response(data)

@api_view(['GET'])
def get_actual(request):
    # Get the absolute path of the directory where this file (views.py) is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the user.json file
    json_file_path = os.path.join(base_dir, 'user.json')

    # Load the data from the user.json file
    try:
        with open(json_file_path, 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

    # Return the data as a JSON response
    return Response(user_data, status=status.HTTP_200_OK)

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

@api_view(['GET'])
def get_summary(request):
    api_key = "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"

    try:
        # Pull all data from the database
        sentiment_analyses = SentimentAnalysis.objects.all()

        # Format the data into a string
        formatted_data = []
        for analysis in sentiment_analyses:
            formatted_data.append(
                f"Restaurant Name: {analysis.name}\n"
                f"Message: {analysis.message}\n"
                f"Analysis:\n"
                f"- Food: {analysis.analysis.get('food', 'N/A')}\n"
                f"- Service: {analysis.analysis.get('service', 'N/A')}\n"
                f"- Atmosphere: {analysis.analysis.get('atmosphere', 'N/A')}\n"
                f"- Cost: {analysis.analysis.get('cost', 'N/A')}\n"
            )
        prompt = "Summarize the following restaurant reviews and their aspects(Convert to percentages from 0-100 (no decimals), (100 good, 0 bad), (an overall average for each aspect), tell the user how review there were for each): \n\n" + "\n\n".join(formatted_data)

        # Initialize the Groq client
        client = Groq(api_key=api_key)

        # Send the prompt to the LLM
        reply = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )

        # Return the summary generated by the LLM
        return Response({
            "summary": reply.choices[0].message.content
        })
    except Exception as e:
        # Handle exceptions and return error response
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)


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