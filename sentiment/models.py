from django.db import models

class Sentiment(models.Model):
    input = models.CharField(max_length=100)
    result = models.CharField(max_length=50)
    def __str__(self):
        return self.result