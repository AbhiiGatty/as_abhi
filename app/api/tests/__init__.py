from .v1 import init_app as init_auth_v1  # Import the versioned routes
from flask import Blueprint

# Create a Blueprint for the auth module
auth_bp = Blueprint('auth', __name__)


def init_app(app):
    """
    Initialize the auth module with the given Flask app.
    Registers the authentication blueprint.
    """
    # Register the versioned auth blueprint
    init_auth_v1(app)
