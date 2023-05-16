import re

# Pre-defined intents and their corresponding responses
intents = {
    'what_is_privacy': 'Privacy is the ability to control what information you share about yourself with others.',
    'how_is_my_data_used': 'Your data is used to improve our services and personalize your experience. We do not share your data with third parties without your consent.',
    'how_is_my_data_protected': 'We take the security of your data seriously and use encryption and other security measures to protect it.',
    'can_i_delete_my_data': 'Yes, you can delete your data at any time by going to your account settings.',
    'what_are_cookies': 'Cookies are small text files that are stored on your device when you visit our website. They help us remember your preferences and provide a better user experience.',
    'how_can_i_manage_cookies': 'You can manage cookies in your browser settings.',
    'default': "I'm sorry, I don't understand. Please try asking a different question."
}

# Regular expressions to match user input to intents
patterns = {
    'what_is_privacy': r'\bprivacy\b|\bprivate\b',
    'how_is_my_data_used': r'\bdata\b|\bused\b',
    'how_is_my_data_protected': r'\bsecurity\b|\bprotected\b',
    'can_i_delete_my_data': r'\bdelete\b|\bdata\b',
    'what_are_cookies': r'\bcookies?\b',
    'how_can_i_manage_cookies': r'\bmanage\b|\bcookies\b',
}

# Function to match user input to intents and return the corresponding response
def get_intent(text):
    for intent, pattern in patterns.items():
        if re.search(pattern, text.lower()):
            return intents[intent]
    return intents['default']

# Example usage
while True:
    user_input = input('You: ')
    response = get_intent(user_input)
    print('Bot:', response)