# listings/views.py
from django.shortcuts import render
from .forms import SentimentForm
from .models import Sentiment
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification

# Load the tokenizer and model from the beshybert folder
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model_path = './beshybert/'
beshybert = TFDistilBertForSequenceClassification.from_pretrained(model_path)

# Define a function that performs sentiment analysis on a given sentence
def perform_sentiment_analysis(sentence):
  # Tokenize the input sentence
  inputs = tokenizer(sentence, return_tensors="tf")

  # Make predictions using the model
  outputs = beshybert(inputs)

  # Get the predicted class (0 or 1) from the logits
  predicted_class = tf.argmax(outputs.logits, axis=1).numpy()[0]

  # Class 0 is negative and class 1 is positive
  sentiment = "positive" if predicted_class == 1 else "negative"

  return sentiment

def sentiment_view(request):
  # If the request is a POST request, validate the user's input and perform sentiment analysis
  if request.method == "POST":
    form = SentimentForm(request.POST)
    if form.is_valid():
      # Get the input from the form
      input = form.cleaned_data["input"]

      # Perform sentiment analysis on the input using your TensorFlow model
      # You can use the code from your previous question here
      result = perform_sentiment_analysis(input)

      # Save the input and result to the database as a Sentiment object
      sentiment = Sentiment(input=input, result=result)
      sentiment.save()

      # Return the result as a response
      return render(request, "home.html", {"form": form, "result": result})
