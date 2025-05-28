PROJECT_NAME=delivery-service
WORKERS=3

up:
	docker-compose up --build

down:
	docker-compose down

run:
	docker-compose up -d

rebuild:
	docker-compose down
	docker-compose up --build

scale:
	docker-compose up --scale worker=$(WORKERS)

migrate:
	docker-compose run --rm alembic

nuke:
	docker-compose down -v --remove-orphans

install:
	poetry install

mypy:
	mypy . --explicit-package-bases

ruff:
	ruff check .
