SHELL := /bin/bash

test:
	cd example && \
	poetry run coverage run --source=image_pattern manage.py test && \
	cd .. && poetry run coverage run --source=image_pattern -m pytest && \
	poetry run coverage combine --append .coverage example/.coverage && \
	poetry run coverage report --fail-under=97 -m && exit
