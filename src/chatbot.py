import random
from settings import Settings


class ChatbotLogic:
    
    def __init__(self, data, gpt_model, intent_model, minimum_confidence_score, privacy_level):
        self.data = data
        self.gpt_model = gpt_model
        self.intent_model = intent_model
        self.minimum_confidence_score = minimum_confidence_score
        self.privacy_level = privacy_level
        self.history = []
        self.dialogue = {'active': False, 'counter': 0}
        self.settings = Settings()

        self.points = self.settings.points

        self.yes_keywords = {'Yes', 'of course', 'yeah', 'sure'}
        self.no_keywords = {'no', 'of course not', 'nope'}
        # Add welcome message
        self.add_bot_response(
            "Hello, I am the iYYU privacy bot. I am here to help you with your questions about the company. What can I help you with today?")

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
        bot_response = self.determine_bot_response(user_message)

        self.add_bot_response(bot_response)

        # if not bot_response.startswith("ChatGPT - "):
        #     time.sleep(1)
        return self.history

    def add_bot_response(self, bot_response):
        self.history.append([None, bot_response])
        return self.history



    def determine_bot_response(self, user_message):
        
        give_suggestion = True
        ### Todo:
        #yes_response and no_response maken, zodat de gebruiker op verschillende manier zijn beslissing kan aanduiden
        '''
        Condition numbers match up with the condition numbers in the chart
        '''
        def update_count(self, count):
            question = self.settings.get_security_level_question(count)
            self.add_bot_response(question)
            return self.dialogue.update({'active': True, 'counter': count})
        count = self.dialogue['counter']

        # question = self.settings.get_security_level_question(count)


        # if self.current_user is None:
        #     return None
        #
        # question_count = self.current_user['points']
        # return self.get_security_level_questions(question_count)

        # Condition 1: Is the dialogue active?
        if (self.dialogue['active']):
            '''
                Use an array of questions to have a dialogue with the user and use the users answers
            '''
            suggestions = True
            response = None
            print("Teststs")
            # 1 pakt counter value



            if count == 0:
                if user_message.lower() == "yes":
                    count += 1
                    update_count(self, count)
                elif user_message.lower() == "no":
                    count += 1
                    self.points = 1  # Set points to 1 when the first "no" is encountered
                    self.settings.add_security_level_points(self.points)
                    update_count(self, count)
                else:
                    response = "Please respond with 'yes' or 'no'!"
                    self.add_bot_response(response)
                    return

            elif count == 1:
                if user_message.lower() == "yes":
                    count += 1
                    update_count(self, count)
                elif user_message.lower() == "no":
                    count += 1
                    self.points += 1  # Increment points for each subsequent "no"
                    self.settings.add_security_level_points(self.points)
                    update_count(self, count)
                else:
                    response = "Please respond with 'yes' or 'no'!"
                    self.add_bot_response(response)
                    return

            elif count == 2:
                self.dialogue.update({"active": False, "counter": 0})
                if user_message.lower() == "yes":
                    if suggestions:
                        self.settings.submit_security_level_estimate(self.points)
                        response = self.settings.generate_advice_response(self.points)
                    else:
                        self.settings.submit_security_level_estimate(self.points)
                        response = self.settings.generate_security_level_response(self.points)
                elif user_message.lower() == "no":
                    if suggestions:
                        self.settings.submit_security_level_estimate(self.points)
                        response = self.settings.generate_advice_response(self.points)
                    else:
                        self.points += 1  # Increment points for the final "no"
                        self.settings.submit_security_level_estimate(self.points)
                        response = self.settings.generate_security_level_response(self.points)
                else:
                    response = "Please respond with 'yes' or 'no'!"
                    self.add_bot_response(response)
                    return

            if response is not None:
                self.add_bot_response(response)


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
                # if intent_name == 'privacy_settings_response':
                #     # 1 pakt counter value
                #     count = self.dialogue['counter']
                #     print(count)
                #
                #     # 2 aan de hand van counter vraagt vraag op
                #
                #     question = self.settings.get_security_level_question(count)
                #     self.add_bot_response(question)
                #     print(user_message)


                # Condition 5: Is there intent that requires a specific action?
                if intent_name == 'privacy_settings_response':
                    # Logic to ask user questions to set the settings here
                    response = None
                    update_count(self, count)

                    # self.dialogue.update({'active': True, 'counter': 0})
                    self.determine_bot_response(user_message)

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
        return response