import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        
        # Defining layers
        self.l1 = nn.Linear(input_size, hidden_size)  # First linear layer
        self.l2 = nn.Linear(hidden_size, hidden_size)  # Second linear layer
        self.l3 = nn.Linear(hidden_size, num_classes)  # Output layer

        # Activation function
        self.relu = nn.ReLU()
    
    def forward(self, x):
        # Pass through first layer + activation
        out = self.l1(x)
        out = self.relu(out)
        
        # Pass through second layer + activation
        out = self.l2(out)
        out = self.relu(out)
        
        # Pass through output layer (no activation)
        out = self.l3(out)
        
        return out
