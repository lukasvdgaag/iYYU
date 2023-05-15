import json


class Settings:
    def __init__(self):
        self.load_user_data()
        self.load_security_levels()
        self.current_user = None

        print('User profiles:', self.user_profiles)
        print('Low security:', self.low_security)
        print('Medium security:', self.medium_security)
        print('High security:', self.high_security)

    def load_user_data(self):
        with open('user_profiles.json', 'r') as file:
            user_profiles = json.load(file)

        self.user_profiles = user_profiles

    def load_security_levels(self):
        with open('user_security_levels.json', 'r') as file:
            user_security_levels = json.load(file)

        # Accessing the values
        self.low_security = user_security_levels['low_security']
        self.medium_security = user_security_levels['medium_security']
        self.high_security = user_security_levels['high_security']

    def set_current_user(self, user_id):
        for user in self.user_profiles:
            if user['user_id'] == user_id:
                self.current_user = user
                break

    def estimate_user_security_level(self):
        if not self.current_user:
            print("No current user set. Please set the current user using set_current_user(user_id).")
            return None

        begin_questions = [
            "Do you want your profile to be high, medium, or low secured?",
            "Do you want help with setting up your account settings?"
        ]

        answers = {}
        security = self.low_security

        for question in begin_questions:
            answer = input(question + " ")
            answers[question] = answer

        permission_change_settings = answers["Do you want help with setting up your account settings?"]
        if permission_change_settings.lower() == "no":
            return security
        else:
            predefined_settings = answers["Do you want your profile to be high, medium, or low secured?"]
            if predefined_settings.lower() == "high":
                security = self.high_security
            elif predefined_settings.lower() == "medium":
                security = self.medium_security

        return security
    

    def update_user_setting(user_id, update_data):
        '''
        This function should be called with the user_id and the setting that should be updated, the answer can be processed here to determine the new value it should have
        or it can be done else where as long as the actual update is done here. This can be done by using a json functionality to update the file
        '''
        return None

    def set_user_calling_card_visibility(user_id, second_user_id):
        '''
        This function should be called with the user_id and the second_user_id and the calling card visibility should be updated
        this can be done by using a json functionality to update the file. As can been seen in the user profiles json, each user has an array that contains objects
        each of the objects contains the id of the user who's the settings are for, as well as the personal visbility for the target user

        Example:
        User Frank (id: 0) want User (Lukas id: 1) to only be able to see select elements of their calling card. This function does that by taking the user id's and updating the
        calling card visiblities accordingly to the intent that's recognised
        '''
        return None
    
    def handle_setting_questions(self) :
        

        return "test"