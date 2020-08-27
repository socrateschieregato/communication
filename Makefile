clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -rf docs/build/

test: clean
	@py.test -x django/communication

coverage: clean
	@py.test -x --cov django/communication --cov-config=.coveragerc --cov-report=term django/communication --cov-report=html --cov-report=xml

detect-migrations:
	@django/manage.py makemigrations --dry-run --noinput --settings=communication.settings.test | grep 'No changes detected' -q || (echo 'Missing migration detected!' && exit 1)

dependencies:
	@pip install -U -r django/requirements/test.txt

migrate:
	@django/manage.py migrate --settings=communication.settings.base

makemigrations:
	@django/manage.py makemigrations --settings=communication.settings.base

run:
	@django/manage.py runserver --settings=communication.settings.base

shell:
	@django/manage.py shell --settings=communication.settings.base

create-app:
	@django/manage.py startapp $(app) --settings=communication.settings.base

superuser:
	@django/manage.py createsuperuser --settings=communication.settings.base

flake8:
	@flake8 --show-source --ignore=W504,F405,F841 .

check-python-import:
	@isort --check

fix-python-import:
	@isort -rc .

fix-clean: clean fix-autopep8

fix-autopep8:
	find . -name '*.py' | grep -v migrations | xargs autopep8 --in-place --ignore=W504,F405,F841

lint: clean flake8 check-python-import

outdated: ## Show outdated dependencies
	@pip list --outdated --format=columns
