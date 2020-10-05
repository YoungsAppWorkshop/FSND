.EXPORT_ALL_VARIABLES:
FLASK_APP=flaskr
FLASK_ENV=development

debug:
	flask run

test:
	pytest

reset:
	dropdb trivia_test
	createdb trivia_test
	psql trivia_test < trivia.psql