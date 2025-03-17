from transformers import pipeline

# Load a small, lightweight chatbot model
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")

def generate_response(message):
    response = chatbot(message, max_length=100, do_sample=True)
    return response[0]["generated_text"]
