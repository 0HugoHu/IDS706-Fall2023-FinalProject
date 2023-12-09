.ONESHELL:
ENV_PREFIX=$(shell python3 -c "if __import__('pathlib').Path('frontend/.venv/bin/pip').exists(): print('frontend/.venv/bin/')")

.PHONY: fmt format
fmt format:              ## Format code using black & isort.
	$(ENV_PREFIX)isort frontend/apps/
	$(ENV_PREFIX)isort microservice/
	$(ENV_PREFIX)black -l 79 frontend/apps/
	$(ENV_PREFIX)black -l 79 frontend/tests/
	$(ENV_PREFIX)black -l 79 microservice/

.PHONY: lint
lint:             ## Run ruff, black, mypy linters.
	$(ENV_PREFIX)ruff frontend/apps/
	$(ENV_PREFIX)black -l 79 --check frontend/apps/
	$(ENV_PREFIX)black -l 79 --check frontend/tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports frontend/apps/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=frontend/apps -l --tb=short --maxfail=10 frontend/tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: install
install:          ## Install the project in dev mode.
	$(ENV_PREFIX)pip3 install --no-cache-dir -r requirements.txt

.PHONY: run
run:              ## Execute the Python code.
	@echo "Running using $(ENV_PREFIX)"
	$(ENV_PREFIX)gunicorn --config frontend/gunicorn-cfg.py frontend/run:apps

