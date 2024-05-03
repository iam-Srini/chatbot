import json
import random
import spacy

# Load the intents data
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Load English language model
nlp = spacy.load('en_core_web_sm')

# Function to preprocess and extract entities from user input
def preprocess_input(text):
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities

def classify_intent(text):
    doc = nlp(text)
    entities = preprocess_input(text)  # Preprocess input text and extract entities
    intent_scores = {}

    for intent in intents['intents']:
        max_similarity = 0
        for pattern in intent['patterns']:
            pattern_doc = nlp(pattern)
            similarity = doc.similarity(pattern_doc)
            max_similarity = max(max_similarity, similarity)
        intent_scores[intent['tag']] = max_similarity

    print(intent_scores)
    classified_intent = max(intent_scores, key=intent_scores.get)
    return classified_intent

# Function to generate response based on classified intent
def generate_response(intent_tag, entities=None):
    for intent in intents['intents']:
        if intent['tag'] == intent_tag:
            response = random.choice(intent['responses'])
            if entities:
                for entity_label, entity_text in entities.items():
                    response = response.replace(f'[{entity_label}]', entity_text)
            return response
    return "Sorry, I didn't understand that."

# Main chatbot function
def chatbot(input_text):
    # Preprocess input and extract entities
    entities = preprocess_input(input_text)
    print(entities)

    # Classify intent based on preprocessed input
    intent_tag = classify_intent(input_text)
    print(intent_tag)

    # Generate response based on classified intent
    response = generate_response(intent_tag, entities)

    return response

# Usage
print("Chatbot: Hi! How can I assist you today?")
while True:
    user_input = input("User: ")
    if user_input.lower() == 'quit':
        print("Chatbot: Goodbye! Have a great day.")
        break
    else:
        bot_response = chatbot(user_input)
        print("Chatbot:", bot_response)