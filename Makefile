# ═══════════════════════════════════════════════════════════════════════
# AI Telegram News Bot — ergonomic Docker entry points
# ═══════════════════════════════════════════════════════════════════════

DOCKER_COMPOSE := docker compose

.PHONY: help up down logs ps build shell test lint health config clean reset

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

up: ## Start the bot (dev override with source mounts)
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up -d

down: ## Stop the bot
	$(DOCKER_COMPOSE) down

logs: ## Tail bot logs
	$(DOCKER_COMPOSE) logs -f --tail=100 bot

ps: ## Show running services
	$(DOCKER_COMPOSE) ps

build: ## Build images (dev target)
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml build

shell: ## Open a shell in the bot container
	$(DOCKER_COMPOSE) exec bot /bin/sh

test: ## Run the repo's test scripts inside the dev image
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml run --rm bot python test_all_scrapers.py
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml run --rm bot python test_bot_logic.py
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml run --rm bot python test_all_commands.py

lint: ## Lint with flake8 (critical errors)
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml run --rm bot python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

health: ## Check bot health via compose healthcheck status
	$(DOCKER_COMPOSE) ps bot

config: ## Validate compose files
	$(DOCKER_COMPOSE) config

clean: ## Stop and remove containers + volumes (cache data loss!)
	$(DOCKER_COMPOSE) down -v --remove-orphans

reset: clean ## Full rebuild from scratch
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml build --no-cache
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up -d
