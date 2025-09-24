.PHONY: install run down

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
	@docker stop chatbot-server