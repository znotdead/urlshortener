build:
	docker-compose build web

run:
	@docker-compose run --rm -p 8000:8000 web python manage.py runserver 0.0.0.0:8000

setup:
	migrate createsuperuser

migrate:
	@docker-compose run --rm web python manage.py migrate

codestyle:
	docker-compose run --rm web pycodestyle .

pylint:
	docker-compose run --rm web prospector .

test:
	docker-compose run --rm web python manage.py test

.PHONY: codestyle pylint build run setup migrate test
