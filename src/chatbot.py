import random
import time
from settings import Settings


class ChatbotLogic:
    
    def __init__(self, data, gpt_model, intent_model, minimum_confidence_score, privacy_level, give_suggestions):
        self.data = data
        self.gpt_model = gpt_model
        self.intent_model = intent_model
        self.minimum_confidence_score = minimum_confidence_score
        self.privacy_level = privacy_level
        self.give_suggestions = give_suggestions
        self.history = []
        self.dialogue = {'active': False, 'counter': 0}
        self.settings = Settings()

        self.yes_keywords = [
            "yes",
            "yeah",
            "yep",
            "yup",
            "sure",
            "absolutely",
            "definitely",
            "certainly",
            "ok",
            "alright",
            "agree",
        ]

        # a list of keywords that indicate a negative answer
        self.no_keywords = [
            "no",
            "nope",
            "nah",
            "not",
            "nay",
            "negative",
            "never",
            "disagree",
            "decline",
            "deny",
            "don't",
        ]


        # Add welcome message
        self.add_bot_response(
            "Hello, I am the iYYU privacy bot. I am here to help you with your questions about the company. What can I help you with today?", False)

    def get_object_by_intent(self, intent):
        for object in self.data:
            if object['intent'] == intent:
                return object
        return None

    def user(self, user_message, history):
        return "", self.add_user_message(user_message)

    def add_user_message(self, user_message):
        self.history.append([user_message, None])

        print(self.history)
        return self.history

    def bot(self, history):
        user_message = self.history[-1][0]
        bot_response, add_delay = self.determine_bot_response(user_message)

        self.add_bot_response(bot_response, delay=add_delay)
        return self.history

    def add_bot_response(self, bot_response, delay=True):
        if delay:
            time.sleep(1)

        self.history.append([None, bot_response])
        return self.history

    def update_count(self, count):
        question = self.settings.get_security_level_question(count)
        self.dialogue.update({'active': True, 'counter': count})
        return question

    def answer_contains_word(self, user_message, keywords):
        user_message = user_message.lower()
        for word in keywords:
            if word in user_message:
                return True
        return False

    def determine_bot_response(self, user_message):
        ### Todo:
        #yes_response and no_response maken, zodat de gebruiker op verschillende manier zijn beslissing kan aanduiden
        '''
        Condition numbers match up with the condition numbers in the chart
        '''
        step = self.dialogue['counter']
        use_gpt = False


        # Condition 1: Is the dialogue active?
        if (self.dialogue['active']):
            '''
                Use an array of questions to have a dialogue with the user and use the users answers
            '''
            response = None
            # 1 pakt counter value

            number_of_questions = len(self.settings.get_all_security_level_questions())

            
            # niet de laatste vraag
            if step < number_of_questions - 1:
                
                if self.answer_contains_word(user_message, self.yes_keywords):
                    step += 1
                    return self.update_count(step), True
                elif self.answer_contains_word(user_message, self.no_keywords):
                    step += 1
                    self.settings.add_security_level_points(1)
                    return self.update_count(step), True
                else:
                    return 'Please answer with yes or no.', True
            else:
                # de laatste vraag
                if self.answer_contains_word(user_message, self.yes_keywords):
                    response = self.settings.generate_security_level_response(self.give_suggestions)
                elif self.answer_contains_word(user_message, self.no_keywords):
                    self.settings.add_security_level_points(1)  # Increment points for the final "no"
                    response = self.settings.generate_security_level_response(self.give_suggestions)
                else:
                    return 'Please answer with yes or no.', True
                
                self.dialogue.update({"active": False, "counter": 0})

        else:
            self.settings.points = 0
            print('2')
            intent_name, confidence_score = self.intent_model.get_intent(question=user_message)
            confidence_score = max(confidence_score)
            intent_data = self.get_object_by_intent(intent_name)
            use_gpt = intent_data['use_gpt']

            print('Prediction:', intent_name, f' ({confidence_score})')

            # test implementation to test whether conversational dialogues work.
            if (user_message == 'lol'):
                intent_name = 'privacy_settings_response'
                confidence_score = 1.0

            # Condition 3: Is the confidence score for the intent high enough to use it?
            if confidence_score < self.minimum_confidence_score:
                print('3: model is not confident on the intent')
                # Condition 4: Does the user have a high or low privacy level?
                if self.privacy_level > 1:
                    # tell user to rephrase
                    print('4: high privact level.')
                    response = "I'm sorry, I'm not sure I understand your question. Could you please rephrase it?"
                else:
                    # send question to ChatGPT
                    print('4: low privacy level.')
                    response = self.gpt_model.answer_question(question=user_message)

            else:
                print('3: model is confident!')
                # Condition 5: Is there intent that requires a specific action?
                if intent_name == 'privacy_settings_response':
                    # Logic to ask user questions to set the settings here
                    response = None
                    self.add_bot_response('Sure, I can help you with that. I will ask you a few questions to determine your desired level of privacy.')
                    return self.update_count(0), False

                elif intent_name == 'change_setting':
                    # NER keywoard recognition implementation here
                    response = '(Test): Specific intent, change specific setting'
                else:
                    print('5: intent is generic')
                    # Condition 6: Is the intent using GPT?
                    if (not use_gpt):
                        # Predefined response
                        print('6: answer should be pre-defined')
                        response = random.choice(intent_data['responses'])
                    else:
                        print('6: ChatGPT should answer.')
                        if self.privacy_level >= 1:
                            prompt_to_send = random.choice(intent_data['responses'])
                            response = self.gpt_model.answer_question(question=prompt_to_send)
                        else:
                            response = self.gpt_model.answer_question(question=user_message)

        # Finally return the response
        return response, not use_gpt