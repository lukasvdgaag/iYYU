import json

class Settings:

    user_data_location = 'assets/user_data.json'

    def __init__(self):
        self.load_user_data()
        self.load_security_levels()
        self.current_user = None
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
        print(data)

        # Find the user with the specified user_id
        for user in data:
            print(user)
            if user['user_id'] == user_id:
                # Update the setting with the new state
                user[setting_name] = setting_state
                break

        # Save the updated JSON data to file
        with open(self.user_data_location, 'w') as file:
            json.dump(data, file)


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

    def get_security_level_question(self, count):
        # Implement the logic to retrieve a security level question based on the count
        # Return the question string
        # Example implementation:
        questions = [
            "Do you want your profile to be published?",
            "Do you want other users to be able to connect with you?",
            "Do you want your account to be visible for search?"
        ]
        if count < len(questions):
            return questions[count]
        else:
            return "No more questions available."

    def add_security_level_points(self, points):
        self.points += points
        
    def generate_advice_response(self, points):
        
        if points == 0 or points == 1:
            self.low_security = True
            self.medium_security = False
            self.high_security = False
            return "You have chosen a low privacy level. Please go to your settings page and open Privacy settings. and make sure all the fields on privacy are turned on"
        elif points == 2:
            self.low_security = False
            self.medium_security = True
            self.high_security = False
            return "You have chosen a medium privacy level. Please go to your settings page and open Privacy settings. Turn off the option for all users to be able to find you, but keep the other options on"
        else:
            self.low_security = False
            self.medium_security = False
            self.high_security = True
            return "You have chosen a high privacy level. Please go to your settings page and open Privacy settings. Make sure all of the settings are turned off."

    def generate_security_level_response(self, points):

        # Text aanpassen

        if points == 0 or points == 1:
            self.low_security = True
            self.medium_security = False
            self.high_security = False
            return "You have chosen a low privacy level. We changed your settings to your preferred combination"
        elif points == 2:
            self.low_security = False
            self.medium_security = True
            self.high_security = False
            return "You have chosen a medium privacy level. We changed your settings to your preferred combination"
        else:
            self.low_security = False
            self.medium_security = False
            self.high_security = True
            return "You have chosen a high privacy level. We changed your settings to your preferred combination"

    def submit_security_level_estimate(self, points):
        user_id = 0  # Change this based on the user's ID
        self.current_user = self.user_profiles.get(user_id)
        if self.current_user:
            if points <= 1:
                new_security_level = self.low_security
            elif points == 2:
                new_security_level = self.medium_security
            else:
                new_security_level = self.high_security

            self.current_user['user_security_level'] = new_security_level

            with open(self.user_data_location, 'w') as file:
                json.dump(list(self.user_profiles.values()), file)

            return "User security level updated to: " + new_security_level
        else:
            return "User not found in user profiles."


def estimate_user_security_level(self):
    '''
    Set up this function to ask the user a bunch of questions, and then based on the answers choose a secutiry level that suits them
    then use the above pre-defined user profile security levels to set their security settings
    since this will be a rule based approach it should just be a bunch of if statements and use the gradio chat to communicate with the user
    '''

    questions = [
        "Do you want your profile to be published?",
        "Do you want other users to be able to connect with you?",
        "Do you want your account to be visible for search?"
    ]
    points = 0

    for question in questions:
        response = input(question + " (yes/no): ")
        if response.lower() == "yes":
            points += 0
        else:
            points += 1

# def set_user_calling_card_visibility(user_id, second_user_id):
#     None
#     with open('user_profiles.json', 'r') as file:
#     user_profiles = json.load(file)

# # Find the user by user_id
# user_index = None
# for i, user in enumerate(user_profiles):
#     if user['user_id'] == user_id:
#         user_index = i
#         break

# if user_index is None:
#     print("User not found.")
#     return

# # Find the user by second_user_id
# second_user_index = None
# for i, viewability in enumerate(user_profiles[user_index]['individual_user_viewability']):
#     if viewability['user_id'] == second_user_id:
#         second_user_index = i
#         break

# if second_user_index is None:
#     print("Second user not found.")
#     return

# visibility = input("Enter visibility (true/false) for the calling card: ")
# visibility = bool(visibility)

# # Update the visibility for the second_user_id
# user_profiles[user_index]['individual_user_viewability'][second_user_index]['profile_card_component_0_visible'] = visibility

# with open('user_profiles.json', 'w') as file:
#     json.dump(user_profiles, file, indent=4)

# def handle_setting_questions(self) :


#     return "test"


# def estimate_user_security_level(self):
#     if not self.current_user:
#         print("No current user set. Please set the current user using set_current_user(user_id).")
#         return None

#     begin_questions = [
#         "Do you want your profile to be high, medium, or low secured?",
#         "Do you want help with setting up your account settings?"
#     ]

#     answers = {}
#     security = self.low_security

#     for question in begin_questions:
#         answer = input(question + " ")
#         answers[question] = answer

#     permission_change_settings = answers["Do you want help with setting up your account settings?"]
#     if permission_change_settings.lower() == "no":
#         return security
#     else:
#         predefined_settings = answers["Do you want your profile to be high, medium, or low secured?"]
#         if predefined_settings.lower() == "high":
#             security = self.high_security
#         elif predefined_settings.lower() == "medium":
#             security = self.medium_security

#     return security

# def set_current_user(self, user_id):
#     for user in self.user_profiles:
#         if user['user_id'] == user_id:
#             self.current_user = user
#             break