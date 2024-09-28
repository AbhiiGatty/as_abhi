# Variables
DOCKER_COMPOSE = docker/docker-compose
APP_CONTAINER = flask-app
MONGO_CONTAINER = mongo

# Targets
.PHONY: build up down restart logs clean

PYTHON_VENV = python_venv

# Targets
.PHONY: build up down clean create-venv

# Create Python virtual environment if it doesn't exist
create-venv:
	@if [ ! -d $(PYTHON_VENV) ]; then \
		python3 -m venv $(PYTHON_VENV); \
		echo "Virtual environment '$(PYTHON_VENV)' created."; \
	else \
		echo "Virtual environment '$(PYTHON_VENV)' already exists."; \
	fi

# Activate the virtual environment
use-venv:
	@echo "Activating virtual environment '$(PYTHON_VENV)'..."
	@source $(PYTHON_VENV)/bin/activate && exec bash

# Stop the virtual environment
stop-venv:
	@echo "To deactivate the virtual environment, run:"
	@echo "  deactivate"

# Build Docker containers
build:
	$(DOCKER_COMPOSE) up --build -d

# Start the services
up:
	$(DOCKER_COMPOSE) up -d

# Stop the services
down:
	$(DOCKER_COMPOSE) down

# Restart the services
restart: down up

# View logs for Flask app and MongoDB
logs:
	$(DOCKER_COMPOSE) logs -f $(APP_CONTAINER) $(MONGO_CONTAINER)

# Clean up containers, networks, and volumes
clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

# Check the status of containers
ps:
	$(DOCKER_COMPOSE) ps
