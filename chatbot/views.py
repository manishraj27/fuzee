import random
import json
import torch
import os
from django.shortcuts import render
from django.http import JsonResponse

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

# Set the device to CUDA (GPU) if available or CPU if not
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Set the model path (from BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'chatbot', 'data.pth')

# Load intents from 'intents.json' which contains training data for the chatbot
with open(os.path.join(BASE_DIR, 'chatbot', 'intents.json'), 'r') as json_data:
    intents = json.load(json_data)

# Load the trained model from the file 'data.pth'
data = torch.load(model_path)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']  # This should match the 'tags' in the trained model
model_state = data["model_state"]

# Initialize the Neural Network model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)  # Load the state of the trained model
model.eval()  # Set the model to evaluation mode

bot_name = "Fuze"

def get_response(msg):
    """Get the chatbot's response based on user input."""

    # Tokenize the message
    sentence = tokenize(msg)

    # Convert the tokens into a bag of words
    X = bag_of_words(sentence, all_words)

    # Reshape the input for the model
    X = X.reshape(1, X.shape[0])

    # Convert to a torch tensor and send to device (GPU or CPU)
    X = torch.from_numpy(X).to(device)

    # Get the model's output
    output = model(X)

    # Get the tag predicted by the model
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]  # Get the tag for the highest prediction

    # Calculate the probabilities of the prediction
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # If the probability of the prediction is above 50%, return the response
    if prob.item() > 0.5:
        for intent in intents['intents']:
            if tag == intent["intent"]:  # Change 'tag' to 'intent'
                # Return a random response from the selected intent
                return random.choice(intent['responses'])

    # Default response if the confidence is low
    return "I do not understand..."


def chat_view(request):
    """Handle the chat interaction via an AJAX request."""
    if request.method == "POST":
        user_message = request.POST.get('user_message')
        
        # Call the get_response function to get the chatbot's reply
        bot_response = get_response(user_message)
        
        # Return the response as JSON
        return JsonResponse({'response': bot_response})
    
    return render(request, 'chat.html')  # Render the initial chat page


def handle_exit_command(sentence):
    """Handle exit commands such as 'quit', 'exit', or 'bye'."""
    exit_commands = ['quit', 'exit', 'bye']
    return sentence.lower() in exit_commands

def home_view(request):
    return render(request, 'home.html')

