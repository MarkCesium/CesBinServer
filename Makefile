docker-build:
	docker compose build

docker-run:
	docker compose up

migration-migrate:
	alembic upgrade head

migration-create:
	alembic revision --autogenerate -m '${msg}'