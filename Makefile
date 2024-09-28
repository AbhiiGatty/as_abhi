# Variables
DOCKER_COMPOSE = docker/docker-compose
APP_CONTAINER = flask-app
MONGO_CONTAINER = mongo

# Targets
.PHONY: build up down restart logs clean

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
