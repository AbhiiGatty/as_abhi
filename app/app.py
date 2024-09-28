from flask import Flask, jsonify
from pymongo import MongoClient

import os
import yaml


# Load configuration from YAML file
def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


# Load the config
config = load_config()

# Set environment variables based on YAML config
MONGO_URI = config['flask']['mongo_uri']


# Setup MongoDB connection
client = MongoClient(MONGO_URI)
db = client['test_db']
collection = db['test_collection']


# Initialize the Flask app
app = Flask(__name__)


@app.route('/')
def index():
    sample_data_dict = {"message": "Welcome to Flask and MongoDB!"}
    collection.insert_one(sample_data_dict)
    return jsonify({"message": "Data inserted into MongoDB!"})


if __name__ == '__main__':
    port = int(config['flask']['port'])
    app.run(host='0.0.0.0', port=port)
