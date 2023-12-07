# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from datetime import datetime

from flask_restx import Resource, Api

import flask
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, generate_token

import boto3

# Bind API -> Auth BP
api = Api(blueprint)


def invoke_lambda_function(function_name, payload):
    client = boto3.client('lambda', region_name='us-east-1')

    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return response
    except Exception as e:
        print(f"Error invoking Lambda function {function_name}: {str(e)}")
        return None


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if flask.request.method == 'POST':

        # read form data
        username = request.form['username']
        password = request.form['password']

        login_response = invoke_lambda_function('dynamodb-lambda-checkloginlambdafunction77404F11-KArjitXGmsrv',
                                                {'username': username, 'password': password})
        login_result = json.loads(login_response['Payload'].read().decode())
        body_content = json.loads(login_result['body'])
        if login_response['StatusCode'] != 200 or body_content['login_successful'] is False:
            return render_template('accounts/login.html',
                                   msg='Wrong user or password',
                                   form=login_form)

        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('authentication_blueprint.route_default'))

    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('accounts/login.html',
                               form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']

        duplicate_response = invoke_lambda_function('dynamodb-lambda-checkduplicateusernamelambdafuncti-abhSKTg7U0CT',
                                                    {'username': username})
        duplicate_result = json.loads(duplicate_response['Payload'].read().decode())
        body_content = json.loads(duplicate_result['body'])
        if body_content['duplicate']:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        add_user_response = invoke_lambda_function('dynamodb-lambda-writetodynamodblambdafunction902BB-gKNxlXgscQ1X',
                                                   {'username': username, 'password': request.form['password']})
        add_user_result = json.loads(add_user_response['Payload'].read().decode())

        if add_user_response['StatusCode'] != 200:
            return render_template('accounts/register.html',
                                   msg='Failed to create user',
                                   success=False,
                                   form=create_account_form)

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@api.route('/login/jwt/', methods=['POST'])
class JWTLogin(Resource):
    def post(self):
        try:
            data = request.form

            if not data:
                data = request.json

            if not data:
                return {
                    'message': 'username or password is missing',
                    "data": None,
                    'success': False
                }, 400
            # validate input
            user = Users.query.filter_by(username=data.get('username')).first()
            if user and verify_pass(data.get('password'), user.password):
                try:

                    # Empty or null Token
                    if not user.api_token or user.api_token == '':
                        user.api_token = generate_token(user.id)
                        user.api_token_ts = int(datetime.utcnow().timestamp())
                        db.session.commit()

                    # token should expire after 24 hrs
                    return {
                        "message": "Successfully fetched auth token",
                        "success": True,
                        "data": user.api_token
                    }
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "success": False,
                        "message": str(e)
                    }, 500
            return {
                'message': 'username or password is wrong',
                'success': False
            }, 403
        except Exception as e:
            return {
                "error": "Something went wrong",
                "success": False,
                "message": str(e)
            }, 500


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
