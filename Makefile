
_config-env:
	[ -f .env ] || cp .env.sample .env

flake8:
	flake8 --exclude=templates,static,venv,tests,migrations

build: _config-env
	docker-compose up -d

stop:
	docker-compose stop

upgrade-pip:
	pip install --upgrade pip

setup: upgrade-pip
	pip install -r requirements-local.txt

start:
	python resenhas/app.py

run:
	start

migrate-init:
	python resenhas/migrate.py db init

migrate:
	python resenhas/migrate.py db migrate

migrate-apply:
	python resenhas/migrate.py db upgrade

migrate-rollback:
	python resenhas/migrate.py db downgrade -1

seed:
	python resenhas/migrate.py seed

# last migrate version c238f53b4e83
