default:help
pr := poetry run
py := $(pr) python
pb := $(pr) pybabel

help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  i		Install deps"
	@echo "  up		Update deps"
	@echo "  migrate	Apply all migrations"
	@echo "  migration	Make new migration with msg='some label'"
	@echo "  run		Start a bot"
	@echo "  flake8		Run flake8 lint"
	@echo "  lang-ext	Extract texts"
	@echo "  lang-up	Update texts"
	@echo "  lang-add	Add new lang with lang='en'"
	@echo "  lang-comp	Compile translates"


# ========
# Commands
# ========

i:
	pip install poetry; poetry install
up:
	poetry update

migrate:
	$(pr) alembic upgrade head
migration:
	$(pr) alembic revision --autogenerate -m "${msg}"

run:
	$(py) -m app

flake8:
	$(py) -m flake8 .

lang-up:
	cd app; $(pb) extract . -o locales/spbxbot.pot; $(pb) update -i locales/spbxbot.pot -d locales -D spbxbot
lang-add:
	cd app; $(pb) init -i locales/spbxbot.pot -d locales -D spbxbot -l ${lang}
lang-comp:
	cd app; $(pb) compile -d locales -D spbxbot
