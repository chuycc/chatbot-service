.PHONY: install run down clean

install:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Docker is not installed. Please install Docker."; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running. Please start the Docker daemon."; \
		exit 1; \
	fi
	@echo "Building Docker image..."
	@docker build -t chatbot-service . >/dev/null 2>&1

run: install
	@echo "Running Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker start chatbot-server >/dev/null 2>&1; \
	else \
		docker run -d --name chatbot-server -p 8000:8000 chatbot-service >/dev/null 2>&1; \
	fi

down:
	@if ! docker info >/dev/null 2>&1; then \
		exit 0; \
	fi; \
	echo "Stopping Docker container..."; \
	if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker stop chatbot-server >/dev/null 2>&1; \
	fi

clean: down
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running. Please start the Docker daemon to remove the container and image."; \
		exit 1; \
	fi
	@echo "Removing Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker rm -f chatbot-server >/dev/null 2>&1; \
	fi
	@echo "Removing Docker image..."
	@if docker images --format '{{.Repository}}' | grep -w "chatbot-service" >/dev/null; then \
		docker rmi -f chatbot-service >/dev/null 2>&1; \
	fi