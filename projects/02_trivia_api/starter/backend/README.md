# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -e .
```

This will install all of the required packages we selected within the `setup.py` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API Endpoints

### GET `/categories`

Endpoint to handle GET requests for all available categories. Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

**Request**:

- Example: `GET /categories`
- URL Parameters: N/A
- Query Parameters: N/A

**Response**:

```json
{
    "data": {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
    },
    "message": "OK",
    "status": 200
}
```

### GET `/questions`

Endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, and categories.

**Request**:

- Example: `GET /questions?page=3`
- URL Parameters: N/A
- Query Parameters:
  - `page`: Current page number. Integer. (Number of questions per page is 10)

**Response**:

```json
{
    "data": {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "questions": [
            {
                "answer": "Yes, it is.",
                "category": 1,
                "difficulty": 1,
                "id": 25,
                "question": "This is a Test Question. Is it working?"
            },
            ...
        ],
        "total_questions": 22
    },
    "message": "OK",
    "status": 200
}
```

### GET `/categories/<int:category_id>/questions`

Endpoint to handle GET requests for questions based on current category, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, and current category.

**Request**:

- Example: `GET /categories/1/questions?page=1`
- URL Parameters:
  - `category_id`: Category ID. Integer.
- Query Parameters:
  - `page`: Current page number. Integer. (Number of questions per page is 10)

**Response**:

```json
{
    "data": {
        "current_category": 1,
        "questions": [
            {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            ...
        ],
        "total_questions": 6
    },
    "message": "OK",
    "status": 200
}
```

### POST `/questions`: Create a new question

Endpoint to handle POST requests for creating new questions. Question, answer, difficulty, category should be submitted to create a new question.

**Request**:

- Example: `POST /questions`
- URL Parameters: N/A
- Query Parameters: N/A
- Payload:

```json
{
    "question": "Where is the best place to learn about programming?",
    "answer": "Udacity",
    "difficulty": 1,
    "category": 1
}
```

**Response**:

```json
{
    "data": {
        "question": {
            "answer": "Udacity",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "Where is the best place to learn about programming?"
        }
    },
    "message": "OK",
    "status": 201
}
```

### DELETE `/questions/<int:question_id>`

Endpoint to handle DELETE requests to remove a question.

**Request**:

- Example: `DELETE /questions/1`
- URL Parameters:
  - `question_id`: Question ID. Integer
- Query Parameters: N/A

**Response**:

```json
{
    "data": {
        "id": 1 // Deleted Question ID
    },
    "message": "OK",
    "status": 200
}
```

### POST `/questions`: Search questions

Endpoint to handle POST requests to get questions based on a search term. It returns any questions of which the search term is a substring.

**Request**:

- Example: `POST /questions`
- URL Parameters: N/A
- Query Parameters: N/A
- Payload:

```json
{
    "searchTerm": "title"
}
```

**Response**:

```json
{
    "data": {
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            ...
        ],
        "totalQuestions": 2
    },
    "message": "OK",
    "status": 200
}
```

### POST `/quizzes`

Endpoint to handle POST requests for getting questions to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

**Request**:

- Example: `POST /questions`
- URL Parameters: N/A
- Query Parameters: N/A
- Payload:

```json
{
    "previous_questions": [11, 12],
    "quiz_category": {"type": "Sports", "id": 6}
}
```

**Response**:

```json
{
    "data": {
        "question": {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    },
    "message": "OK",
    "status": 200
}
```

## Testing

To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
pytest
```
