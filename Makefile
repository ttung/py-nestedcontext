include common.mk
MODULES=src tests

lint:
	flake8 $(MODULES)

mypy:
	mypy --ignore-missing-imports $(MODULES)

test_srcs := $(wildcard tests/test_*.py)

test: lint mypy
	coverage run --source=src/nestedcontext -m unittest discover tests -v

fast_test: lint mypy $(test_srcs)

$(test_srcs): %.py :
	python -m unittest $@

.PHONY: test lint mypy $(test_srcs)
