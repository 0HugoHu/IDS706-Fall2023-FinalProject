from datetime import datetime
from functools import wraps

import jwt
from flask import request, current_app

from apps.authentication.models import Users


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        else:
            return {
                       'message': 'Token is missing',
                       'data': None,
                       'success': False
                   }, 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['user_id']).first()
            if current_user is None:
                return {
                           'message': 'Invalid token',
                           'data': None,
                           'success': False
                       }, 403
            now = int(datetime.utcnow().timestamp())
            init_date = data['init_date']

            # if now - init_date > 24 * 3600:  # expire token after 24 hours
            #    return {
            #               'message': 'Expired token',
            #               'data': None,
            #               'success': False
            #           }, 403

        except Exception as e:
            return {
                       'message': str(e),
                       'data': None,
                       'success': False
                   }, 500
        return func(*args, **kwargs)

    return decorated
