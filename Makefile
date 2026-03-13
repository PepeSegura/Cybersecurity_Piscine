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

src-ssh:
	docker exec -it source /bin/bash

target-ssh:
	docker exec -it target /bin/bash

attacker-ssh:
	docker exec -it attacker /bin/bash

src-info:
	@docker inspect source -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'

target-info:
	@docker inspect target -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}'

restart:: stop
restart:: start

logs:
	$(COMPOSE) -p $(PROJECT_NAME) logs -f

ps:
	$(COMPOSE) -p $(PROJECT_NAME) ps

prune:
	docker system prune -af
	docker volume prune -af

clean:
	$(COMPOSE) down --rmi all --volumes --remove-orphans
