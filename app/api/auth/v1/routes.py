from flask import Blueprint, request, jsonify
from app.api.auth.models import User
from app.utils.jwt_utils import generate_access_token, generate_refresh_token, decode_token
from app.middleware.auth_middleware import token_required
from app.cache.redis import set_refresh_token, delete_refresh_token

auth_v1_bp = Blueprint('auth_v1', __name__)


@auth_v1_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic validation
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required."}), 400

    # Check if the user already exists
    if User.objects(username=username):
        return jsonify({"error": "Username already exists."}), 400

    if User.objects(email=email):
        return jsonify({"error": "Email already exists."}), 400

    # Create a new user instance
    user = User(username=username, email=email)
    user.set_password(password)  # Hash the password
    user.save()  # Save the user to the database

    return jsonify({"message": "User registered successfully."}), 201


@auth_v1_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Find user by email
    user = User.objects(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    # Generate access and refresh tokens
    access_token = generate_access_token(user.username, user.roles)
    refresh_token = generate_refresh_token(user.username)

    # Store refresh token with expiration time in Redis (30 days)
    expires_in_seconds = 30 * 24 * 60 * 60  # 30 days
    set_refresh_token(user.email, access_token, expires_in_seconds)

    return jsonify(id=str(user.id), access_token=access_token, refresh_token=refresh_token), 200


@auth_v1_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_token():
    """Generate a new access token using the refresh token."""
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({"error": "Refresh token is required."}), 400

    payload = decode_token(refresh_token)

    if payload is None:
        return jsonify({"error": "Invalid or expired refresh token."}), 401

    # Generate new access token
    access_token = generate_access_token(payload['sub'], payload['roles'])

    return jsonify(access_token=access_token), 200


@auth_v1_bp.route('/logout', methods=['POST'])
@token_required
def logout_user():
    token = request.token  # Access the token from the request object

    if not token:
        return jsonify({"error": "Access token is required."}), 400

    # Remove the refresh token from Redis
    delete_refresh_token(token)

    return jsonify({"message": "User logged out successfully."}), 200
