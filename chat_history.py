class ChatHistory:

    def __init__(self):
        self.history = []

    def add_message(self, message, role):
        self.history.insert(0, ChatHistory.Message(message=message,role=role))

    def get_latest_message(self):
        return self.history[0]
    
    def get_latest_user_message(self):
        return next((msg for msg in self.history if msg.get_role() == "user"), None)

    def get_latest_bot_message(self):
        return next((msg for msg in self.history if msg.get_role() == 'bot'), None)

    def get_history(self):
        return self.history
    
    class Message:
        def __init__(self, message, role, intent = None):
            self.message = message
            self.role = role,
            self.intent = intent

        def get_message(self) -> str:
            return self.message
    
        def get_role(self) -> str:
            return self.role
        
        def get_intent(self) -> str:
            return self.intent