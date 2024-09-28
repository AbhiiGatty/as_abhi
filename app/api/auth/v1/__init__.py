from flask import Blueprint
from .routes import auth_v1_bp


def init_app(app):
    app.register_blueprint(auth_v1_bp, url_prefix='/api/v1/auth')
