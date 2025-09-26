IMAGE_NAME := chatbot-service
CONTAINER_NAME := chatbot-server

.PHONY: install run down clean, help, test

help:
	@echo "Available commands:"
	@echo "  install  - Install all requirements to run the service"
	@echo "  run      - Run the service and all related services in Docker"
	@echo "  down     - Teardown of all running services"
	@echo "  clean    - Teardown and removal of all containers"
	@echo "  test     - Run tests"

install: clean
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Docker is not installed. Please install Docker."; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running. Please start the Docker daemon."; \
		exit 1; \
	fi
	@echo "Building Docker image..."
	@if ! docker build -t $(IMAGE_NAME):latest . >/dev/null 2>&1; then \
		echo "Docker build failed. Please visit https://www.dockerstatus.com"; \
		exit 1; \
	fi

run: install
	@if lsof -i :8000 >/dev/null 2>&1; then \
		echo "Error: Port 8000 is already in use. Please free the port and try again."; \
		exit 1; \
	fi
	@echo "Running Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "$(CONTAINER_NAME)" >/dev/null; then \
		docker start $(CONTAINER_NAME) >/dev/null 2>&1; \
	else \
		docker run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME) >/dev/null 2>&1; \
	fi

down:
	@if ! docker info >/dev/null 2>&1; then \
		exit 0; \
	fi; \
	echo "Stopping Docker container..."; \
	if docker ps -a --format '{{.Names}}' | grep -w "$(CONTAINER_NAME)" >/dev/null; then \
		docker stop $(CONTAINER_NAME) >/dev/null 2>&1; \
	fi

clean: down
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running. Please start the Docker daemon to remove the container and image."; \
		exit 1; \
	fi
	@echo "Removing Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "$(CONTAINER_NAME)" >/dev/null; then \
		docker rm -f $(CONTAINER_NAME) >/dev/null 2>&1; \
	fi
	@echo "Removing Docker image..."
	@if docker images --format '{{.Repository}}' | grep -w "$(IMAGE_NAME)" >/dev/null; then \
		docker rmi -f $(IMAGE_NAME):latest >/dev/null 2>&1; \
	fi

test:
	@echo "Running tests..."
	@if ! command -v pytest >/dev/null 2>&1; then \
		echo "pytest is not installed. Please install pytest to run tests."; \
		exit 1; \
	fi
	@pytest