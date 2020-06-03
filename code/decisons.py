
class Decisions:
    def __init__(self, user, profile_gender, socre, gender_intent, last_modified, last_match, is_active, is_positive, has_canceled, \
         last_connection, connection_history, selected, negative_match, age, country_school):
        self.user = user
        self.profile_gender = profile_gender
        self.score = socre
        self.gender_intent = gender_intent
        self.last_modified = last_modified
        self.last_match = last_match
        self.is_active = is_active
        self.is_positive = is_positive
        self.has_canceled = has_canceled
        self.last_connection = last_connection
        self.connection_history = connection_history
        self.selected = selected
        self.negative_match = negative_match
        self.age = age
        self.country_school = country_school

    #建立两个用户的联系
    def build_connection(self, user):
        if user.user in self.connection_history:
            return False
        else:
            self.connection_history.add(user.user)
            user.connection_history.add(self.user)
            return True
            
    #打印 user profile
    def print_info(self):
        print(">>>>>>>")
        print("ID:", self.user, "\n")
        print("Gender:", self.profile_gender, "\n")
        print("Age:", self.age, "\n")
        print("Gender Intent:", self.gender_intent, "\n")
        print("Is positive?:", self.is_positive,"\n")
        print("Last Modified:",self.last_modified, "\n")
        print("Connection History:", self.connection_history, "\n")
        print("Negative Match:", self.negative_match, "\n")
        print("Country & School:", "China" if self.country_school[0] == 1 else "USA", self.country_school[1], "\n")
        print(">>>>>>>")