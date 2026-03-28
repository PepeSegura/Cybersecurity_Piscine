COMPOSE_FILE := _docker/docker-compose.yml

PROJECT_NAME := inquisitor

COMPOSE := docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME)

up:
	- $(COMPOSE) up --build -d

down:
	- $(COMPOSE) down

build:
	- $(COMPOSE) build

start:
	- $(COMPOSE) start

stop:
	- $(COMPOSE) stop

restart: stop start


ssh-src:
	- $(COMPOSE) exec -it source /bin/bash

ssh-target:
	- $(COMPOSE) exec -it target /bin/bash

ssh-attacker:
	- $(COMPOSE) exec -it attacker /bin/bash


INFO_SRC = $(COMPOSE) -p $(PROJECT_NAME) ps -q source | xargs docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'
INFO_TARGET = $(COMPOSE) -p $(PROJECT_NAME) ps -q target | xargs docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'

info-src:
	@echo "$$( $(INFO_SRC) )"
	
info-target:
	@echo " $$( $(INFO_TARGET) )"

info:
	@echo "python3 inquisitor.py $$( $(INFO_SRC) ) $$( $(INFO_TARGET) )"


logs:
	- $(COMPOSE) -p $(PROJECT_NAME) logs -f

ps:
	- $(COMPOSE) -p $(PROJECT_NAME) ps

prune:
	- docker image prune -a -f
	- docker system prune -f
	- docker volume prune -a -f

clean:
	- $(COMPOSE) down --rmi all --volumes --remove-orphans

clean-all: stop clean prune

.PHONY: up down build start stop restart
.PHONY: ssh-src ssh-target ssh-attacker info-src info-target info
.PHONY: logs ps prune clean clean-all
