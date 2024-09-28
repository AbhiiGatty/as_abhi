from flask import Flask, jsonify
import os
import yaml
from app import create_app


def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


# Load the config
config = load_config()

# Initialize the Flask app
app = create_app()

# Set Flask config values
app.config.update(
    MONGO_URI=config['flask']['mongo_uri'],
    SECRET_KEY=config['flask']['jwt_secret_key'],  # Load the secret key
    PORT=config['flask']['port']
)


@app.route('/ping', methods=['GET'])
def ping():
    """Ping route to check server health."""
    return jsonify({"message": "Pong!"}), 200


if __name__ == '__main__':
    PORT = config['flask'].get('port', 5000)  # Default to 5000 if not specified
    app.run(host='0.0.0.0', port=PORT)
