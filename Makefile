.PHONY: install run down clean

install:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Docker is not installed. Please install Docker."; \
		exit 1; \
	fi
	@echo "Building Docker image..."
	@docker build -t chatbot-service .

run:
	@echo "Running Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker start chatbot-server; \
	else \
		docker run -d --name chatbot-server -p 8000:8000 chatbot-service; \
	fi

down:
	@echo "Stopping Docker container..."
	@if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker stop chatbot-server; \
	fi

clean:
	@echo "Removing Docker container and image"
	@if docker ps -a --format '{{.Names}}' | grep -w "chatbot-server" >/dev/null; then \
		docker stop chatbot-server; \
		docker rm -f chatbot-server; \
	fi
	@if docker images --format '{{.Repository}}' | grep -w "chatbot-service" >/dev/null; then \
		docker rmi -f chatbot-service; \
	fi