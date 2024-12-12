from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

sentiment_analyzer = pipeline("text-classification", model="srimeenakshiks/aspect-based-sentiment-analyzer-using-bert")

sentence = "The food here is great and definitely worth the price. The cost is reasonable for the quality, and the restaurant has a nice vibe. However, the service felt a bit rushed, which impacted the overall experience. Still, a solid spot for a good meal!"

aspect = "service"

formatted_input = f"{sentence} Aspect: {aspect}"
result = sentiment_analyzer(formatted_input)

tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

for aspect in ['service']:
    print(f"Aspect: {aspect}")
    
    # Get classifier result for the current aspect
    classifier_result = classifier(sentence, text_pair=aspect)
    print("deBERTa Research Result:", classifier_result)
    
    # Process and label the sentiment analysis result from srimeenakshiks model
    for item in result:
        if item['label'] == 'LABEL_0':
            item['label'] = 'Negative'  
        elif item['label'] == 'LABEL_1':
            item['label'] = 'Positive'  
    
    print("IMDB BERT Model Result:", result)
