# AISentimentAnalysisApp

Dependencies for this backend api
Python Version 3.12 (not 3.13)

Installation:
Create .env files 
Activate .env 

install the following:
```bash
pip install transformers, tiktoken, sentencepiece, django, protobuf, djangorestframework, groq, django-cors-headers
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

start server:
```
python manage.py runserver
```

Installing frontend
```
cd frontend
npm init es6
npm install
```

start frontend:
```
npm run dev
```

This project is an aspect-based sentiment analysis tool designed specifically for analyzing restaurant reviews. It uses advanced AI techniques to determine the sentiment of customer feedback across multiple aspects of the dining experience. These aspects can include key elements such as food quality, service, ambiance, price, and more.

By breaking down reviews into specific categories, the tool provides a more granular analysis of customer sentiments, allowing restaurant owners and stakeholders to gain deeper insights into what their customers truly think. This can help businesses understand strengths and weaknesses in particular areas, such as whether their food quality is highly praised while their service might need improvement.

The tool is capable of identifying positive, negative, or neutral sentiments for each aspect, helping businesses make data-driven decisions to enhance their customer experience.

API:
/api/view.py - Most of the API code is located here

POST:
/api/v1/analysis/

GET:
/api/v1/data/
/api/v1/summary/
/api/v1/actual/

Slides:
https://docs.google.com/presentation/d/1UKTBaV-GaNSiMCGOiz8JVnzA_XMPzUHu/edit?usp=sharing&ouid=114992111180774571887&rtpof=true&sd=true