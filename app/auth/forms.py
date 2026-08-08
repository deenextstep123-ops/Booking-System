
from app.extensions import db
from app.models import User
import re

# registration form class gets data from whatever form has been filled out and validates it

class RegistrationForm:

    def __init__(self,data):
        self.first_name = data['first_name'].strip()
        self.last_name = data['last_name'].strip()
        self.email = data['email'].lower().strip()
        self.password = data['password']
        self.username = data['username'].strip().lower()
        self.confirm_password = data['confirm_password']

        self.errors = []





    def validate_username(self):

        if len(self.username) < 3:
            self.errors.append("Username must be at least 3 characters")
            return False

        if len(self.username) > 20:
            self.errors.append("Username must be at most 20 characters")
            return False


        regex = r"[a-z0-9_\-]+"
        if not re.fullmatch(regex,self.username):
            self.errors.append("Username can only contain letters, numbers, underscores and hyphens")
            return False

        # query the database, check if username already exists in the database

        user = db.session.scalar(
            db.select(User).where(User.username == self.username)
        )

        #scalar selects the user with the username, if no user is found it returns none

        if user is not None:
            self.errors.append("Username already taken")
            return False

        return True





    def validate_email(self):


        regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,15}"
        if not re.fullmatch(regex,self.email):
            self.errors.append("Invalid email address")
            return False

        if len(self.email) > 120:
            self.errors.append("Email too long (120 characters)")
            return False

        existing_user = db.session.scalar(
            db.select(User).where(User.email == self.email)
        )

        if existing_user is not None:
            self.errors.append("email already taken")
            return False
        return True

    def validate_password(self):

        if len(self.password) < 8:
            self.errors.append("Password must be at least 8 characters")
            return False

        if self.password == self.confirm_password:
            return True

        else:
            self.errors.append("Passwords do not match")
        return False

    def validate_first_name(self):

        if len(self.first_name) == 0:
            self.errors.append("First name must not be empty")
            return False

        if len(self.first_name) > 50:
            self.errors.append("first name must be at most 50 characters")
            return False

        regex = r"[A-Za-z'\- ]+"

        if not re.fullmatch(regex, self.first_name):
            self.errors.append("First name must only be valid characters")
            return False

        return True

    def validate_last_name(self):

        if len(self.last_name) == 0:
            self.errors.append("Last name must not be empty")
            return False

        if len(self.last_name) > 50:
            self.errors.append("Last name must be at most 50 characters")
            return False

        regex = r"[A-Za-z'\- ]+"

        if not re.fullmatch(regex, self.last_name):
            self.errors.append("Last name must only be valid characters")
            return False
        return True

    def validate(self):

        #clear whatever error messages are already there
        self.errors.clear()

        self.validate_email()
        self.validate_first_name()
        self.validate_last_name()
        self.validate_password()
        self.validate_username()

        if not self.errors:
            return True

        return False


        # return if not self.errors will run the same, just easier to read like this

class LoginForm():
    def __init__(self,data):
        self.user = data['user'].strip().lower()
        self.password = data['password']

        self.errors = []


    # validate identifier returns either a user object or none
    # it's checking to see if the username of email can be found in the database,
    # it's 'none' if it cant find any, or if it does find one then return that user object
    def validate_identifier(self) -> User | None:

        existing_user = db.session.scalar(
            db.select(User).where(User.email == self.user)
        )

        if existing_user is not None:
            return existing_user

        existing_user = db.session.scalar(
            db.select(User).where(User.username == self.user)
        )

        if existing_user is not None:
            return existing_user

        self.errors.append("Invalid username/email or password")
        return None


    # validate password takes a user object and returns a bool

    def validate_password(self,existing_user: User) -> bool:
        if not existing_user:
            return False
        if not existing_user.check_password(self.password):
            self.errors.append("Invalid username/email or password")
        else:
            return True
        return False

    def validate(self):
        self.errors.clear()

        user = self.validate_identifier()
        if user is None:
            return False

        if self.validate_password(user):
            return user

        return False

