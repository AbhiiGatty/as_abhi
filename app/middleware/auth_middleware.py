# app/auth/middleware.py

from flask import request, jsonify
from functools import wraps
from app.utils.jwt_utils import decode_token
from app.cache.redis import get_user_email_by_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is missing."}), 401

        token = auth_header.split(" ")[1]  # Get token from 'Bearer <token>'
        payload = decode_token(token)

        if payload is None:
            return jsonify({"error": "Invalid or expired token."}), 401

        # Check if token exists in cache
        res = get_user_email_by_token(token)
        if res is None:
            return jsonify({"error": "Invalid token."}), 401

        # Optionally, you can attach the user information to the request object
        request.user = payload  # This will allow you to access user data in the route
        request.token = token
        return f(*args, **kwargs)

    return decorated


role_access_map = {
    'admin': ['/api/v1/tests'],
    # 'user': ['/api/v1/tests'],
}


def admin_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is missing."}), 401

        token = auth_header.split(" ")[1]  # Get token from 'Bearer <token>'
        payload = decode_token(token)

        if payload is None:
            return jsonify({"error": "Invalid or expired token."}), 401

        # Check if token exists in cache
        res = get_user_email_by_token(token)
        if res is None:
            return jsonify({"error": "Invalid token."}), 401

        roles = payload.get('roles')
        for role in roles:
            if role in role_access_map.keys():
                if request.path not in role_access_map[role]:
                    return jsonify({"error": "You do not have permission to access this resource."}), 403
                else:
                    break
            else:
                return jsonify({"error": "You do not have permission to access this resource."}), 403

        # Optionally, you can attach the user information to the request object
        request.user = payload  # This will allow you to access user data in the route
        request.token = token
        return f(*args, **kwargs)

    return decorated
