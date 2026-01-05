from transformers import pipeline
classifier=pipeline("sentiment-analysis")
texts="I don't like this code"
result=classifier(texts)
print("Sentiment of text",result)