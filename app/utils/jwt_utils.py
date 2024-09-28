import jwt
import datetime
from flask import current_app


def generate_access_token(email, roles, expires_delta=datetime.timedelta(minutes=15)):
    payload = {
        'sub': str(email),
        'roles': list(roles),
        'exp': datetime.datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def generate_refresh_token(email, expires_delta=datetime.timedelta(days=30)):
    payload = {
        'sub': str(email),
        'exp': datetime.datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
