from django.db import models

class SentimentAnalysis(models.Model):
    message = models.TextField(unique=True)
    analysis_result = models.JSONField()  # or use TextField to store results as JSON string

    def __str__(self):
        return self.message