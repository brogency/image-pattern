SHELL := /bin/bash

test:
	cd django_example && \
	poetry run coverage run --source=image_pattern manage.py test && \
	cd .. && poetry run coverage run --source=image_pattern -m pytest && \
	poetry run coverage combine --append .coverage django_example/.coverage && \
	poetry run coverage report --fail-under=97 -m && exit
