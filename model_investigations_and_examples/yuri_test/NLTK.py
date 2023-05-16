# import nltk
# from nltk.tokenize import word_tokenize

# # Define some sample intents and their associated training phrases
# intents = {
#     'greeting': ['hello', 'hi', 'hey there'],
#     'goodbye': ['bye', 'goodbye', 'see you later'],
#     'weather': ['what\'s the weather like today?', 'will it rain today?']
# }

# # Define a function to determine the intent of a given user message
# def determine_intent(user_message):
#     tokens = word_tokenize(user_message.lower())
#     for intent, training_phrases in intents.items():
#         for phrase in training_phrases:
#             if all(word in tokens for word in word_tokenize(phrase.lower())):
#                 return intent
#     return None

# # Test the function with some sample user messages
# print(determine_intent('Hello, how are you?')) # Output: greeting
# print(determine_intent('What is the forecast for today?')) # Output: weather
# print(determine_intent('See you later!')) # Output: goodbye

print('hi')