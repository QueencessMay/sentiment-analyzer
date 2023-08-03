# sentiment/views.py
from django.shortcuts import render
from .forms import SentimentForm
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model_path = 'FiouReia/beshybert'
beshybert = TFDistilBertForSequenceClassification.from_pretrained(model_path)

def home(request):
  if request.method == "POST":
    form = SentimentForm(request.POST)
    if form.is_valid():
      input_text = form.cleaned_data["input"]

      try:
        result = perform_sentiment_analysis(input_text)
      except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        result = "Error occurred"

      return render(request, "sentiment/home.html", {"form": form, "result": result})
  else:
    form = SentimentForm()

  return render(request, "sentiment/home.html", {"form": form})

def perform_sentiment_analysis(sentence):
  if not sentence:
    return "Invalid input"

  inputs = tokenizer(sentence, return_tensors="tf")

  outputs = beshybert(inputs)

  predicted_class = tf.argmax(outputs.logits, axis=1).numpy()[0]

  sentiment = "positive" if predicted_class == 1 else "negative"

  return sentiment