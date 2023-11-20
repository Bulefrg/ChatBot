import json
import re
import random_responses
from datetime import datetime
import spacy


nlp = spacy.load("en_core_web_lg")  # or "en_core_web_sm"

print("maded by Bulef43")

def load_json(file):
    with open(file, encoding='utf-8') as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


response_data = load_json("bot.json")

def semantic_similarity(token1, token2):
    return token1.similarity(token2)
print("hello can i help you ?")

def similar_word_in_list(word, word_list):
    for w in word_list:
        if semantic_similarity(nlp(word), nlp(w)) > 0.7:  # Adjust the similarity threshold as needed
            return True
    return False

def get_response(input_string):
    # Check for time-related query
    if any(word in input_string.lower() for word in ["time"]):
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Use spaCy for better understanding of user input
    input_tokens = nlp(input_string.lower())

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_words_set = set(response["required_words"])

        # Check if there are any required words
        if required_words_set:
            for token in input_tokens:
                if any(similar_word_in_list(token.text, required_words_set) for word in response["required_words"]):
                    response_score += 1

        # Amount of required words should match the required score
        if response_score == len(required_words_set):
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if similar_word_in_list(word, response["user_input"]):
                    response_score += 1

        # Add score to list
        score_list.append(response_score)

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()

while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))