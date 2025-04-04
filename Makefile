.PHONY: format lint up down build restart logs shell

format:
	black --line-length 79 --skip-string-normalization .
	ruff check . --fix


lint:
	ruff check .

# Docker Compose
up:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down -v

restart:
	docker compose down -v && docker compose up --build

logs:
	docker compose logs -f

shell:
	docker compose exec web /bin/bash