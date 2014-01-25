from flask_wtf import Form
from flask import flash, session
from wtforms import (TextField, SubmitField, PasswordField, HiddenField,
                     validators)
from models import User, Show, UserShows


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
        email = User.query.filter_by(email=self.email.data.lower()).first()
        if email:
            self.email.errors.append("That email is already taken.")
            return False
        user = User.query.filter(User.username.ilike(self.username.data))\
            .first()
        if user:
            self.username.errors.append("That username is taken.")
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

        user = User.query.filter(User.username.ilike(self.username.data))\
            .first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid username or password")
            return False


class AddShow(Form):  # Corresponds to add_shows.html
    show_name = TextField("Show Name:", [validators.Required("Please enter"
                          " a show name.")])
    search = SubmitField("Search")
    show_id = HiddenField()
    submit = SubmitField("Add Show")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

# TODO: Work out some better form validation in this section, for christ's sake.

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True
# Determine if show already exists for the user

    def validate_unique(self):
        user = User.query.filter_by(username=session.get('username')).first()
        show = UserShows.query.filter_by(user=user.id)\
            .filter_by(show=Show.query.filter_by(tmdb_id=self.show_id.data)
            .first().id).first()
        if show:
            # Why can't I append to errors here?
            return False

        else:
            return True


