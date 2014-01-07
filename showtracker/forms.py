from flask_wtf import Form
from wtforms import TextField, SubmitField, PasswordField, validators
from models import User


class SignupForm(Form):
    username = TextField("Username", [validators.Required("Username Please.")])
    email = TextField("Email", [validators.Required("Enter an address."),
                      validators.Email("Please enter a valid email address")])
    password = PasswordField("Password", [validators.Required("Password Plz")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        # Checks that all validators are happy
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.")
            return False
        else:
            return True


class LoginForm(Form):
    username = TextField("Username", [validators.Required("Please enter"
                         " a username")])
    password = PasswordField("Password", [validators.Required("Please enter"
                             " a password")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid username or password")
            return False
