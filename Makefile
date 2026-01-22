PROJECT = tcp_ip
SRC := $(shell find $(PROJECT) -type f -name '*.py')
PYTHON := $(shell peotry env info -e)

all: lint test

lint:
	ruff check ./${PROJECT}/
	pylint ./${PROJECT}/

test:
	pytest -vv tests/

format:
	ruff format ./${PROJECT}/

clean_python:
	@rm -rf ./dist

clean:
	@echo clean

.PHONY: all lint format test clean_python clean