.EXPORT_ALL_VARIABLES:
FLASK_APP=flaskr
FLASK_ENV=development

init:
	psql trivia < flaskr/trivia.psql

install:
	pip install -e .

reset:
	dropdb trivia_test
	createdb trivia_test
	psql trivia_test < flaskr/trivia.psql

run:
	flask run

test: reset
	pytest
