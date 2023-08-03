from django.forms import ModelForm
from .models import Sentiment

class SentimentForm(ModelForm):
    class Meta:
        model = Sentiment
        fields = '__all__'