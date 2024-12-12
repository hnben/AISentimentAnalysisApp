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

This is a aspect based sentiment analysis tool to analysze resturants 

API:
POST:
/api/v1/analysis/



GET:
/api/v1/data/
/api/v1/summary/
/api/v1/actual/

Slides:
https://docs.google.com/presentation/d/13-Pydworp58jAzbyzu7gd35OkKZFUhK30ely0t8CL9k/edit?usp=sharing