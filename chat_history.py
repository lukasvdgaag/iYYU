class ChatHistory:

    def __init__(self):
        self.history = []

    def add_message(self, message, role, intent, setting_update, chatbot_answer):
        self.history.insert(
            0,
            ChatHistory.Message(
                message=message,
                role=role,
                intent=intent,
                setting_update=setting_update,
                chatbot_answer=chatbot_answer,
            ),
        )

    def get_latest_message(self):
        return self.history[0]
    
    def get_latest_user_message(self):
        for msg in self.history:
            if msg.get_role() == "user":
                return msg.get_message()
        return None

    def get_latest_bot_message(self):
        for msg in self.history:
            if msg.get_role() == "bot":
                return msg
        return None

    def get_history(self):
        return self.history
    
    class Message:
        def __init__(self, message, role, intent = None, setting_update = None , chatbot_answer = None):
            self.message = message
            self.role = role,
            self.intent = intent
            self.setting_update = setting_update
            self.chatbot_answer = chatbot_answer

        def get_message(self):
            return self.message
    
        def get_role(self):
            return self.role
        
        def get_intent(self):
            return self.intent