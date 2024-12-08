import random
import json
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Set the device to CUDA (GPU) if available or CPU if not
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents from 'intents.json' which contains training data for the chatbot
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load the trained model from the file 'data.pth'
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
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

    # If the probability of the prediction is above 75%, return the response
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["intent"]:
                # Return a random response from the selected intent
                return random.choice(intent['responses'])
    
    # Default response if the confidence is low
    return "I do not understand..."


def handle_exit_command(sentence):
    """Handle exit commands such as 'quit', 'exit', or 'bye'."""
    exit_commands = ['quit', 'exit', 'bye']
    return sentence.lower() in exit_commands


if __name__ == "__main__":
    print(f"{bot_name}: Hello! How can I assist you today? (type 'quit', 'exit', or 'bye' to end)")
    
    # Start an infinite loop to keep the conversation going
    while True:
        sentence = input("You: ")  # Get input from the user
        
        # If the user wants to exit, break the loop
        if handle_exit_command(sentence):
            print(f"{bot_name}: Goodbye! Have a great day!")
            break

        # Get the chatbot's response based on the input sentence
        response = get_response(sentence)
        
        # Output the response to the user
        print(f"{bot_name}: {response}")

