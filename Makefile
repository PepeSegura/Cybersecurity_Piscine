CONFIG=docker-compose.yml

COMPOSE = docker compose -f $(CONFIG)

up:
	$(COMPOSE) up --build

build:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

exec:
	$(COMPOSE) exec sand-box /bin/bash

all: up

re:: prune
re:: all

prune:
	- docker image prune -a -f
	- docker system prune -f
	- docker volume prune -a -f

.PHONY: build up exec all prune re