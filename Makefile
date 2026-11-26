# Project commands. On Windows, run them with `mingw32-make <target>` or install GNU make.
# Every target goes through uv, so the locked environment (uv.lock) is always used.

GROUP ?= footrating

.PHONY: install format lint test requirements check zip

install:  ## Create .venv from uv.lock and install the pre-commit hooks
	uv sync --frozen
	uv run pre-commit install

format:  ## Auto-format and fix imports
	uv run ruff format src tests scripts
	uv run ruff check --fix src tests scripts

lint:  ## Lint and check formatting (no changes)
	uv run ruff check src tests scripts
	uv run ruff format --check src tests scripts

test:  ## Run the test suite
	uv run pytest

requirements:  ## Regenerate requirements.txt from uv.lock
	uv export --no-hashes --format requirements-txt -o requirements.txt

check: lint test  ## Lint + tests; exit code 0 only if everything passes

zip:  ## Build Group_$(GROUP)_DS_Project.zip (default: Group_footrating_DS_Project.zip) without data/ or models
	uv run python scripts/make_zip.py --group $(GROUP)
