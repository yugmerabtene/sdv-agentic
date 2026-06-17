.PHONY: install install-dev lint test test-cov run docker-build docker-run clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	flake8 app/ tests/
	black --check app/ tests/

format:
	black app/ tests/

typecheck:
	mypy app/ --ignore-missing-imports

security:
	bandit -r app/ -x app/templates

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=term --cov-report=html

run:
	flask run --host=0.0.0.0 --port=5000 --reload

docker-build:
	docker build -t nexa-social .

docker-run:
	docker run -p 5000:5000 -v $(PWD)/data:/app/data nexa-social

docker-compose-up:
	docker compose up -d

docker-compose-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage

all: install-dev lint typecheck security test
