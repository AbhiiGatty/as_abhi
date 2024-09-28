from flask import Flask
from app.api.auth import init_app as init_auth
from app.db.mongodb import initialize_db
import yaml


def load_config():
    """Load configuration from a YAML file."""
    config_file = 'config.yaml'
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)


def create_app():
    app = Flask(__name__)

    # Load and set the configuration from the YAML file
    config = load_config()
    app.config.update(config['flask'])  # Update Flask's config with the loaded config

    # Initialize MongoDB with the loaded URI
    initialize_db(app.config['mongo_uri'])  # Assuming 'mongo_uri' is defined in your config

    # Register versioned auth blueprint
    init_auth(app)

    return app
