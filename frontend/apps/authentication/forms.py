# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email

# login and registration


class LoginForm(FlaskForm):
    username = StringField(
        "Username", id="username_login", validators=[DataRequired()]
    )
    password = PasswordField(
        "Password", id="pwd_login", validators=[DataRequired()]
    )


class CreateAccountForm(FlaskForm):
    username = StringField(
        "Username", id="username_create", validators=[DataRequired()]
    )
    password = PasswordField(
        "Password", id="pwd_create", validators=[DataRequired()]
    )
