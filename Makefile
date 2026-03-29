.DEFAULT_GOAL := help

.PHONY: help install run api test lint format clean docker-build docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make install      Instala dependencias con uv"
	@echo "  make run          Ejecuta el orquestador (modo interactivo)"
	@echo "  make api          Levanta la API FastAPI en localhost:8000"
	@echo "  make test         Ejecuta los tests con pytest"
	@echo "  make lint         Verifica el codigo con ruff"
	@echo "  make format       Formatea el codigo con ruff"
	@echo "  make docker-build Construye la imagen Docker"
	@echo "  make docker-up    Levanta los servicios con docker-compose"
	@echo "  make docker-down  Detiene los servicios"
	@echo "  make clean        Elimina archivos temporales"

install:
	uv sync

run:
	uv run python src/main.py

api:
	uv run uvicorn api.Router.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ tests/ api/

format:
	uv run ruff format src/ tests/ api/

docker-build:
	docker build -t multi-system-agent .

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
