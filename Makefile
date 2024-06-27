SHELL=/bin/bash
VIRTUALENV?=.venv
PORT?=3000
.PHONY: help install freeze clean venvclean llama3 gpt4 gpt4o opus combine

help:
	@echo "Make targets:"
	@echo " install     Create virtual environment (.venv) and install required packages"
	@echo " freeze      Persist installed packages to requirements.txt"
	@echo " clean       Remove *.pyc files and __pycache__ directory"
	@echo " venvclean   Remove virtual environment(s)"
	@echo " llama3      Run llama3.py"
	@echo " gpt4        Run gpt4.py"
	@echo " gpt4o       Run gpt4o.py"
	@echo " opus        Run opus.py"
	@echo "Check the Makefile for more details"

install:
	@python3 -m venv $(VIRTUALENV)
	@. $(VIRTUALENV)/bin/activate; pip3 install --upgrade pip; pip3 install -r requirements.txt

freeze:
	@. $(VIRTUALENV)/bin/activate; pip3 freeze > requirements.txt

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} \+

venvclean: clean
	@rm -rf $(VIRTUALENV)

llama3:
	@. $(VIRTUALENV)/bin/activate; python3 src/llama3.py

gpt4:
	@. $(VIRTUALENV)/bin/activate; python3 src/gpt4.py

gpt4o:
	@. $(VIRTUALENV)/bin/activate; python3 src/gpt4o.py

opus:
	@. $(VIRTUALENV)/bin/activate; python3 src/opus.py

combine:
	@. $(VIRTUALENV)/bin/activate; python3 utils/combine.py --data "test" --model "opus"
