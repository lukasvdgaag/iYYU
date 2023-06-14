import json

class Settings:

    user_data_location = 'assets/user_data.json'

    def __init__(self):
        self.user_id = '0'

        self.load_user_data()
        self.load_security_levels()

        # print(self.user_profiles)

        self.current_user = self.user_profiles.get(self.user_id)
        self.points = 0

        # print('User profiles:', self.user_profiles)
        # print('Low security:', self.low_security)
        # print('Medium security:', self.medium_security)
        # print('High security:', self.high_security)

    def load_user_data(self):
        with open(self.user_data_location, 'r') as file:
            user_profiles = json.load(file)
        self.user_profiles = {user['user_id']: user for user in user_profiles}

    def load_security_levels(self):
        with open('assets/user_security_levels.json', 'r') as file:
            user_security_levels = json.load(file)
        self.low_security = user_security_levels['low_security']
        self.medium_security = user_security_levels['medium_security']
        self.high_security = user_security_levels['high_security']

    def update_user_setting(self, user_id, setting_name, setting_state):
        '''
        This function should be called with the user_id and the setting that should be updated, the answer can be processed here to determine the new value it should have
        or it can be done else where as long as the actual update is done here. This can be done by using a json functionality to update the file
        '''
        with open(self.user_data_location, 'r') as file:
            data = json.load(file)

        # print(user_id, setting_name, setting_state)

        for user in data:
            if user['user_id'] == user_id:
                if setting_state == 'enable':
                    setting_state = True
                elif setting_state == 'disable':
                    setting_state = False
                else:
                    return False
                user[setting_name] = setting_state
                break
        else:
            return False  # User not found

        with open(self.user_data_location, 'w') as file:
            json.dump(data, file)
        return True


    def set_user_calling_card_visibility(self, user_id, individual_user_id, profile_card_component, component_state):
        '''
        This function should be called with the user_id and the second_user_id and the calling card visibility should be updated
        this can be done by using a json functionality to update the file. As can been seen in the user profiles json, each user has an array that contains objects
        each of the objects contains the id of the user who's the settings are for, as well as the personal visbility for the target user

        Example:
        User Frank (id: 0) want User (Lukas id: 1) to only be able to see select elements of their calling card. This function does that by taking the user id's and updating the
        calling card visiblities accordingly to the intent that's recognised
        '''
        with open(self.user_data_location, 'r') as file:
            data = json.load(file)

        for user in data:
            if user.get('user_id') == user_id:
                # Find the target user in individual_user_viewability
                for target_user in user['individual_user_viewability']:
                    if target_user.get('user_id') == individual_user_id:
                        # Update the calling card component visibility for the target user
                        if profile_card_component in target_user:
                            target_user[profile_card_component] = component_state
                            user_found = True
                            break

        with open(self.user_data_location, 'w') as file:
            json.dump(data, file)

    def get_all_security_level_questions(self):
        return [
            "Do you want your profile to be publicly visible?",
            "Are you open to accepting new connections from other users?"
        ]

    def get_security_level_question(self, count):
        # Implement the logic to retrieve a security level question based on the count
        # Return the question string
        # Example implementation:
        questions = self.get_all_security_level_questions()
        if count < len(questions):
            return questions[count]
        else:
            return "No more questions available."

    def add_security_level_points(self, points):
        self.points += points
        
    def get_security_level_from_points(self, points):
        return points +1
        
    def get_settings_from_security_level(self, level):
        if level == 1:
            return self.low_security
        elif level == 2:
            return self.medium_security
        else:
            return self.high_security

    def generate_advice_response(self, level):
        if level == 1:
            return "You have chosen a low privacy level. Please go to your settings page and open Privacy settings. and make sure all the fields on privacy are turned on"
        elif level == 2:
            return "You have chosen a medium privacy level. Please go to your settings page and open Privacy settings. Turn off the option for all users to be able to find you, but keep the other options on"
        else:
            return "You have chosen a high privacy level. Please go to your settings page and open Privacy settings. Make sure all of the settings are turned off."

    def generate_security_level_response(self, give_suggestions):
        level = self.get_security_level_from_points(self.points)

        if give_suggestions:
            return self.generate_advice_response(level)

        else:
            new_settings = self.get_settings_from_security_level(level)
            self.current_user.update(new_settings)

            with open(self.user_data_location, 'w') as file:
                json.dump(list(self.user_profiles.values()), file)

            if level == 1:
                return "You have chosen a low privacy level. We changed your settings to your preferred combination"
            elif level == 2:
                return "You have chosen a medium privacy level. We changed your settings to your preferred combination"
            else:
                return "You have chosen a high privacy level. We changed your settings to your preferred combination"