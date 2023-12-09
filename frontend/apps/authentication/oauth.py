# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from apps.config import Config
from flask import current_app as app
from flask import flash, redirect, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import github, make_github_blueprint
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound

from .models import OAuth, Users, db

github_blueprint = make_github_blueprint(
    client_id=Config.GITHUB_ID,
    client_secret=Config.GITHUB_SECRET,
    scope="user",
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    info = github.get("/user")

    if info.ok:
        account_info = info.json()
        username = account_info["login"]

        query = Users.query.filter_by(oauth_github=username)
        try:
            user = query.one()
            login_user(user)

        except NoResultFound:
            # Save to db
            user = Users()
            user.username = "(gh)" + username
            user.oauth_github = username

            # Save current user
            db.session.add(user)
            db.session.commit()

            login_user(user)
