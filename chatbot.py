class ChatbotLogic:
    def __init__(self, data, gpt_model, intent_model, minimum_confidence_score, privacy_level):
        self.data = data
        self.gpt_model = gpt_model
        self.intent_model = intent_model
        self.minimum_confidence_score = minimum_confidence_score
        self.privacy_level = privacy_level
        self.history = []
        self.dialogue = {'active': False, 'counter': 0}

        # Add welcome message
        self.add_bot_response("Hello, I am the iYYU privacy bot. I am here to help you with your questions about the company. What can I help you with today?")
        
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
        '''
        Condition numbers match up with the condition numbers in the chart
        
        '''
        # Condition 1: Is the dialogue active?
        if (self.dialogue['active']):
            '''
                Use an array of questions to have a dialogue with the user and use the users answers
            '''
            response = '(Test): Starting dialogue'

            # Condition 2: Are there dialogue questions left?
            dialogue_questions = ['test', 'test2', 'test3']
            if (self.dialogue.counter < len(dialogue_questions)):
                response = '(Test): More dialogue questions'
            else:
                response = '(Test): Ran out of dialogue questions, computing answer then awaiting user input'

        else:
            print('2')
            intent_name, confidence_score = self.intent_model.get_intent(question=user_message)
            confidence_score = max(confidence_score)
            intent_data = self.get_object_by_intent(intent_name)
            use_gpt = intent_data['use_gpt']
            generate_context = True

            # Condition 3: Is the confidence score for the intent high enough to use it?
            if confidence_score < self.minimum_confidence_score:
                print('3: model is not confident on the intent')
                # Condition 4: Does the user have a high or low privacy level?
                if self.privacy_level >= 1: 
                    print('4: high privact level.')
                    response = '(Test): Low confidence, high security answer'
                else:
                    print('4: low privacy level.')
                    response = '(Test): Low confidence, low security answer (use chatgpt)'
            else:
                print('3: model is confident!')
                # Condition 5: Is there intent that requires a specific action?
                if intent_name == 'initalize_user_settings':
                    # Logic to ask user questions to set the settings here
                    response = '(Test): Specific intent, initialize settings'
                elif intent_name == 'change_setting':
                    # NER keywoard recognition implementation here
                    response = '(Test): Specific intent, change specific setting'
                else:
                    print('5: intent is generic')
                    # Condition 6: Is the intent using GPT?
                    if (not use_gpt):
                        print('6: answer should be pre-defined')
                        # Predefined response
                        response = '(Test): Send the predefined response (settings respones)'
                    else:
                        print('6: ChatGPT should answer.')
                        if self.privacy_level >= 1: 
                            response = '(Test): Send predefined question to chatgpt'
                        else:
                            response = '(Test): Send users questions directly to chatgpt'


        # Finally return the response
        return response