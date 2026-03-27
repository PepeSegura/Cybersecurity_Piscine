COMPOSE_FILE := _docker/docker-compose.yml

PROJECT_NAME := inquisitor

COMPOSE := docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME)

.PHONY: up down build start stop restart logs ps prune shell-source shell-target shell-attacker

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

start:
	$(COMPOSE) start

stop:
	$(COMPOSE) stop

ssh-src:
	$(COMPOSE) exec -it source /bin/bash

ssh-target:
	$(COMPOSE) exec -it target /bin/bash

ssh-attacker:
	$(COMPOSE) exec -it attacker /bin/bash

info-src:
	@docker inspect source -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'

info-target:
	@docker inspect target -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'

restart:: stop
restart:: start

logs:
	$(COMPOSE) -p $(PROJECT_NAME) logs -f

ps:
	$(COMPOSE) -p $(PROJECT_NAME) ps

prune:
	- docker image prune -a -f
	- docker system prune -f
	- docker volume prune -a -f

clean:
	$(COMPOSE) down --rmi all --volumes --remove-orphans
