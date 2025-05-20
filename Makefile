APP = app

.PHONY: migrate
migrate:
	docker exec -it ${APP} python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker exec -it ${APP} python manage.py makemigrations logic

.PHONY: up
up: 
	docker compose up --build

.PHONY: createsuperuser
createsuperuser:
	docker exec -it ${APP} python manage.py createsuperuser
