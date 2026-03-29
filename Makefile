.DEFAULT_GOAL := help

.PHONY: help install run test lint format clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install   Instala dependencias con uv"
	@echo "  make run       Ejecuta el orquestador (modo interactivo)"
	@echo "  make test      Ejecuta los tests con pytest"
	@echo "  make lint      Verifica el codigo con ruff"
	@echo "  make format    Formatea el codigo con ruff"
	@echo "  make clean     Elimina archivos temporales"

install:
	uv sync

run:
	uv run python src/main.py

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
