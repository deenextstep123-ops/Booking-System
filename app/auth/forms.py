from app.models import User

class RegistrationForm:
    def validate_username(self,username):
        # another thing
        # validate code goes here
        pass

    def validate_email(self,email):
        # another
        pass

    def save_user(self,username,email,password,first_name,last_name):
        user = User(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)