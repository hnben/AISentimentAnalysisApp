from django.db import models

class SentimentAnalysis(models.Model):
    name = models.CharField(max_length=255, default="Unknown") 
    message = models.TextField()
    analysis = models.JSONField(default=dict)

    def __str__(self):
        return self.name