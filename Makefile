dc = docker compose
pfa = --profile auth
pfc = --profile celery

dcprod = $(dc) -f docker-compose-prod.yaml
dcdev = $(dc)

up:
	$(dcdev) $(pfa) {$pfc} up -d --build

up-billing:
	$(dcdev) up -d --build

up-celery:
	$(dcdev) $(pfc) up -d --build

up-auth:
	$(dcdev) $(pfa) up -d --build

downv:
	$(dcdev) $(pfa) $(pfc) down -v

down:
	$(dcdev) $(pfa) $(pfc) down

create-admin:
	$(dcdev) exec auth_service python -m cli admin create $(email) $(password)

env:
	./env-setup.sh

p-up:
	$(dcprod) up -d --build

p-downv:
	$(dcprod) down -v

p-down:
	$(dcprod) down

p-create-admin:
	$(dcprod) exec auth_service python -m cli admin create $(email) $(password)