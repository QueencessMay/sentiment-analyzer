# sentiment/forms.py
from django import forms

class SentimentForm(forms.Form):
    input = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Enter a comment'}))