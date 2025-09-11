.PHONY: ci-local venv install test clean lint-actions ci-check clean-artifacts

# Python interpreter; override with `make PY=python3.10 ci-local` if needed
PY ?= python3
VENV := venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

venv:
	@$(PY) -m venv $(VENV)
	@$(VENV)/bin/python -m pip install --upgrade pip

install: venv
	@$(PIP) install -r requirements.txt
	@$(PIP) install -r requirements_dev.txt

test: install
	@PYTHONPATH="$$PYTHONPATH:./bk_resource:./tests" \
	DJANGO_SETTINGS_MODULE=tests.settings \
	BK_APP_CONFIG_PATH=tests.config \
	$(PYTEST) -vs tests --disable-warnings --cov=.

ci-local:
	@$(MAKE) --no-print-directory test; ec=$$?; \
	sleep 1; \
	$(MAKE) --no-print-directory clean-artifacts; \
	exit $$ec

clean-artifacts:
	rm -rf .pytest_cache .mypy_cache htmlcov \
		.coverage coverage.xml .coverage.*

clean: clean-artifacts
	rm -rf dist build

# Lint GitHub Actions workflows with actionlint
lint-actions:
	@command -v actionlint >/dev/null 2>&1 || { \
		echo "actionlint not found. Install with: brew install actionlint"; \
		exit 1; \
	}
	@actionlint -color

# Run both actionlint and tests
ci-check: lint-actions test
