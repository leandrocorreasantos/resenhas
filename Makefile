_config-env:
	[ -f .env ] || cp .env.sample .env

flake8:
	flake8 --exclude=templates,static,venv,tests,migrations

build: _config-env
	docker-compose up -d

stop:
	docker-compose down

upgrade-pip:
	pip install --upgrade pip

setup: upgrade-pip
	pip install -r requirements-local.txt

run:
	flask run

start: run

migrate-init:
	flask db init

migrate:
	flask db migrate

migrate-apply:
	flask db upgrade

migrate-rollback:
	flask db downgrade -1
