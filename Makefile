PROJECT = luftqualitaet_sachsen
PORT ?= 8000
ENV ?= dev
PERIOD ?= 24H

WHERE = $(shell uname -a)
ifeq ($(CI),true)
PYTHON_PATH = $(BUILD_DIR)/$(PROJECT)
else
PYTHON_PATH = $(shell pwd)/$(PROJECT)
endif

.PHONY: help install install-dev install-test install-osx create-db \
			info isort isort-check test coverage coverage-html migrate \
			runserver shell docs clean clean-coverage clean-pyc fetch

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install            to install/update all packages required for production"
	@echo "  install-dev        to install/update all packages required for development (includes production)"
	@echo "  install-test       to install/update all packages required for testing (includes production)"
	@echo "  install-osx        to install/update the packages required for OS X"
	@echo "  create-db          to create a new PostgreSQL user and database"
	@echo "  isort              to run isort on the whole project"
	@echo "  isort-check        to check the whole project with isort"
	@echo "  test               to run the tests with pytest"
	@echo "  coverage           to generate a coverage report"
	@echo "  coverage-html      to generate and open a HTML coverage report"
	@echo "  migrate            to synchronize Django's database state with the current set of models and migrations"
	@echo "  runserver          to start Django's development Web server"
	@echo "  shell              to start a Python interactive interpreter"
	@echo "  docs               to build and open the project documentation as HTML"
	@echo "  clean              to remove all artifacts"
	@echo "  clean-coverage     to remove coverage artifacts"
	@echo "  clean-pyc          to remove Python file artifacts"
	@echo "  fetch              to fetch live data"

install:
	pip install -U --no-deps -r requirements/prod.txt

install-dev:
	pip install -U --no-deps -r requirements/dev.txt

install-test:
	pip install -U --no-deps -r requirements/test.txt

install-osx:
	pip install -U --no-deps -r requirements/osx.txt

create-db:
	createuser -d -e -P luftqualitaet_sachsen
	createdb -U luftqualitaet_sachsen luftqualitaet_sachsen

info:
	@echo "Testing on $(WHERE)"

isort:
	isort --recursive $(PROJECT)

isort-check:
	isort --check-only --recursive $(PROJECT)

test: info
	PYTHONPATH=$(PYTHON_PATH) py.test --pep8 --flakes $(TEST_ARGS) $(PROJECT)

coverage: info
	PYTHONPATH=$(PYTHON_PATH) py.test --pep8 --flakes $(TEST_ARGS) --cov-config=$(PROJECT)/.coveragerc --cov $(PROJECT) $(PROJECT)

coverage-html: coverage
	coverage html
	@python -c "import os, webbrowser; webbrowser.open('file://%s/htmlcov/index.html' % os.getcwd())"

migrate:
	envdir envs/$(ENV) $(PROJECT)/manage.py migrate

runserver:
	envdir envs/$(ENV) $(PROJECT)/manage.py runserver $(PORT)

shell:
	envdir envs/$(ENV) $(PROJECT)/manage.py shell

docs:
	$(MAKE) -C docs clean html
	@python -c "import os, webbrowser; webbrowser.open('file://%s/docs/_build/html/index.html' % os.getcwd())"

clean: clean-coverage clean-pyc

clean-coverage:
	rm -f .coverage
	rm -fr htmlcov

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-release:
	rm -fr release

fetch:
	envdir envs/$(ENV) $(PROJECT)/manage.py fetch $(PERIOD)
