import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import json

# Initialize the stemmer
stemmer = PorterStemmer()

# Function to tokenize a sentence
def tokenize(sentence):
    """
    Tokenizes a sentence into words/tokens
    """
    return nltk.word_tokenize(sentence)

# Function to stem a word to its base form
def stem(word):
    """
    Stem a word to its root form (e.g., 'running' -> 'run')
    """
    return stemmer.stem(word.lower())

# Function to create a bag of words from a tokenized sentence and a list of known words
def bag_of_words(tokenized_sentence, words):
    """
    Creates a bag of words representation for a sentence
    """
    # Stem each word in the sentence
    sentence_words = [stem(word) for word in tokenized_sentence]
    
    # Initialize a bag with zeros for each word in the 'words' list
    bag = np.zeros(len(words), dtype=np.float32)
    
    # Set 1 if the word is present in the sentence
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
    
    return bag

# Load the intent.json file
def load_intents():
    """
    Loads the intents from the provided JSON file
    """
    with open("intent.json", "r") as file:
        intents = json.load(file)
    return intents

# Extract all words from the intents
def extract_all_words(intents):
    """
    Extract all words from the intents to build the vocabulary
    """
    all_words = []
    for intent in intents['intents']:
        for example in intent['examples']:
            tokenized_sentence = tokenize(example)
            all_words.extend(tokenized_sentence)
    
    # Stem all words and remove duplicates
    all_words = [stem(w) for w in all_words]
    all_words = sorted(list(set(all_words)))  # Remove duplicates and sort
    return all_words

# Process all intents and create the bag of words for each example
def process_intents(intents, all_words):
    """
    Process the intents to create the bag of words for each example
    """
    training_sentences = []
    training_labels = []
    output_empty = [0] * len(all_words)
    
    for intent in intents['intents']:
        for example in intent['examples']:
            # Tokenize and stem each example sentence
            tokenized_sentence = tokenize(example)
            
            # Create the bag of words for this sentence
            bag = bag_of_words(tokenized_sentence, all_words)
            
            # Append the bag of words and the label (intent)
            training_sentences.append(bag)
            training_labels.append(intent['intent'])
    
    return np.array(training_sentences), np.array(training_labels)

# Main function to execute everything
def main():
    # Load intents
    intents = load_intents()
    
    # Extract all words (vocabulary)
    all_words = extract_all_words(intents)
    
    # Process intents and get the training data
    training_sentences, training_labels = process_intents(intents, all_words)
    
    print("Training Sentences (Bag of Words):")
    print(training_sentences)
    
    print("\nTraining Labels (Intents):")
    print(training_labels)

if __name__ == "__main__":
    main()
