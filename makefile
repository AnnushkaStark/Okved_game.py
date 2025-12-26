ci:
	ruff format
	ruff check --fix

PYTHON = python3
ENV = .env
PIP = venv/bin/pip

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt


run:
	@echo "🎮 Запуск ОКВЭД-Квеста..."
	$(PYTHON) game/main.py

.PHONY: tests
tests:
	ENV=TEST pytest --cov=game
