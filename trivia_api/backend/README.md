# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## API Documentation
We use this documentation to list all endpoints and method that you can use in this app.

### URL: http://127.0.0.1:5000/
This app can only run locally use flask and has not deployed to any host, so the home url is http://127.0.0.1:5000/ by Python Flask app.
### Available Endpoints


                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /questions    |  [x] |  [x]  |   [x]   |         
      /categories   |  [x] |       |         |           
      /quizzes      |      |  [x]  |         | 


### 1. GET /questions

Fetch paginated questions:
```bash
$ GET http://127.0.0.1:5000/questions
```
- Fetches a list of dictionaries of questions in which the keys are the ids and number of total questions.
- Request Arguments: 
    - **integer** `page` (optional)
- Request Headers: **None**
- Returns: 
  1. List of dict of questions 
  2. **integer** `total_questions`
  3. **boolean** `success`

#### Example response
```js
{
"categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"current_category": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
}

```
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"search" : "royal"}' -H 'Content-Type: application/json'
```
- Fetch questions that contain value of key `search` 
- Request: Json body, key is `search` and value is content
- Return：List of questions that contain the content
#### Example response
```js
{
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_question": 1
}

```
Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "1+2", "category" : "1" , "answer" : "3", "difficulty" : 1 }' -H 'Content-Type: application/json'
```
- Create a new Question
- Request:Question, Category ID, Answer, and difficulty
- Return all questions like GET ./questions

###3. DELETE Question

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on given id
- Request Arguments: 
  - **integer** `question_id`
- Returns: success status, question id deleted, all other questions and total questions

#### Example response
```js
{
  "deleted": 10, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    [...]
  "success": true, 
  "total_questions": 20
}
```
###4. POST quiz
```bash
curl -X POST http://127.0.0.1:5000/quiz -d '{"previous_questions" : [1], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- provide a list of already asked questions and a category to ask for a fitting, random question.
- Request: previous_questions, quiz_category
- Return: a random question
#### Example response
```
{
  "question": {
    "answer": "3", 
    "category": 1, 
    "difficulty": 1, 
    "id": 25, 
    "question": "1+2"
  }, 
  "success": true
}
```

###5. GET Category
### 5. GET /categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a list of all `categories` with its `type` as values.
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example response
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
