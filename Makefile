dc = docker compose
pfa = --profile auth
pfc = --profile celery
pfn = --profile notification

dcprod = $(dc) -f docker-compose-prod.yaml
dcdev = $(dc)

up:
	$(dcdev) $(pfa) $(pfc) $(pfn) up -d --build

up-billing:
	$(dcdev) up -d --build

up-celery:
	$(dcdev) $(pfc) up -d --build

up-auth:
	$(dcdev) $(pfa) up -d --build

up-notification:
	$(dcdev) $(pfn) $(pfa) up -d --build

downv:
	$(dcdev) $(pfa) $(pfc) $(pfn) down -v

down:
	$(dcdev) $(pfa) $(pfc) $(pfn) down

create-admin:
	$(dcdev) exec auth_service python -m cli admin create $(email) $(password)

create-templates:
	$(dcdev) exec notification_admin python -m cli template create-templates

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