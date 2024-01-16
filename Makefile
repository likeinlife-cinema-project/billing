up:
	docker compose up -d --build

downv:
	docker compose down -v

down:
	docker compose down

env:
	./env-setup.sh

prod-up:
	docker compose -f docker-compose-prod.yaml up -d --build

prod-downv:
	docker compose -f docker-compose-prod.yaml down -v

prod-down:
	docker compose -f docker-compose-prod.yaml down

create-admin:
	docker compose exec auth_service python -m cli admin create $(email) $(password)
