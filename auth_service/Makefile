freeze:
	poetry export -o src/requirements.txt --without-hashes

test:
	docker compose -f tests/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from tests --attach tests

down-test:
	docker compose -f tests/docker-compose.yaml down

