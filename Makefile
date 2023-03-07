SHELL := /bin/bash

f = docker-compose.yml

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null

push:
	pip install -r requirements.txt
	python3 main.py
