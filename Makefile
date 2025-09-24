.PHONY: install

install:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Docker is not installed. Please install Docker."; \
		exit 1; \
	fi
	@echo "Building Docker image..."
	@docker build -t chatbot-service .