from flask import Blueprint
from .routes import test_v1_bp


def init_app(app):
    app.register_blueprint(test_v1_bp, url_prefix='/api/v1/tests')
