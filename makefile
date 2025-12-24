ci:
	ruff format
	ruff check --fix

PYTHON = python3
ENV = .env

run:
	@echo "🎮 Запуск ОКВЭД-Квеста..."
	$(PYTHON) game/main.py
