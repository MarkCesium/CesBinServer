docker-build:
	docker build . -t cesbinserver

docker-run:
	docker run -p 8000:8000 cesbinserver

migration-migrate:
	alembic upgrade head

migration-create:
	alembic revision --autogenerate -m '${msg}'