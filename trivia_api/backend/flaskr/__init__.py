import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  Done: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # --------------------------------------------------#
    # helper functions
    # --------------------------------------------------#
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_question = questions[start:end]

        return current_question

    def getErrorMessage(error, default_text):
        try:
            # Return message contained in error, if possible
            return error.description["message"]
        except TypeError:
            # otherwise, return given default text
            return default_text

    '''
  Done: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def retrive_categories():

        all_category = Category.query.all()
        if not all_category:
            abort(404)
        all_category = [category.format()['type'] for category in all_category]
        return jsonify({
            "success": True,
            "categories": all_category
        })

    '''
  Done: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions', methods=['GET'])
    def retrive_questions():
        selection = Question.query.order_by(Question.id).all()
        current_question = paginate_questions(request, selection)
        if len(current_question) == 0:
            abort(404)

        categories = {category.id: category.type for category in Category.query.all()}
        current_category = list(set([categories.get(question.category, 'unknown') for question in selection]))

        return jsonify(
            {
                "success": True,
                "questions": current_question,
                "total_questions": len(Question.query.all()),
                "current_category": current_category,
                "categories": categories
            })

    '''
  Done: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_book(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(400, {'message': 'id {} question does not exists'.format(question_id)})

        try:
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                }
            )
        except:
            abort(422)

    '''
  Done: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    '''
  additionall Done: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        if not body:
            abort(400, {'message': 'request not found'})
        searchTerm = body.get("searchTerm", None)
        if searchTerm:
            questions = Question.query.filter(Question.question.contains(searchTerm)).all()

            if not questions:
                abort(404, {"message": 'no questions which contains {} found.'.format(searchTerm)})

            questions_found = [question.format() for question in questions]
            selections = Question.query.order_by(Question.id).all()
            categories = Category.query.all()
            # categories_all = [category.format() for category in categories]

            return jsonify({
                'success': True,
                'questions': questions_found,
                'total_questions': len(selections),
                'current_category': ''
            })

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = str(int(body.get('category', None)) + 1)
        new_difficulty = body.get('difficulty', None)

        try:
            # Try to insert a new question. If anything went wrong, raise 422 "unprocessable"
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()

            # After succesfully insertion, get all paginated questions
            selections = Question.query.order_by(Question.id).all()
            questions_paginated = paginate_questions(request, selections)

            # Return succesfull response
            return jsonify({
                'success': True,
                'created': question.id,
                'questions': questions_paginated,
                'total_questions': len(selections)
            })
        except:
            abort(422)

    '''
  Done: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        selection = Question.query.filter(Question.category == str(category_id)).order_by(Question.id).all()
        current_question = paginate_questions(request, selection)
        if not current_question:
            abort(400, {'message': 'id {} category does not exists'.format(category_id)})

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(selection),
            'current_category': category_id
        })

    '''
  Done: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        if not body:
            abort(400, {'message': 'request not found'})
        previous_questions = body.get('previous_questions', None)
        current_category = body.get('quiz_category', None)
        if current_category['type'] == 'click':
            current_category = None

        if not previous_questions:
            if current_category:
                questions_raw = Question.query.filter(Question.category == str(int(current_category['id'])+1)).all()
            else:
                questions_raw = Question.query.all()
        else:
            if current_category:
                questions_raw = Question.query.filter(Question.category == str(int(current_category['id'])+1)) \
                    .filter(Question.id.notin_(previous_questions)) \
                    .all()
            else:
                questions_raw = Question.query \
                    .filter(Question.id.notin_(previous_questions)) \
                    .all()

        questions_formatted = [question.format() for question in questions_raw]

        if len(questions_formatted) == 1:
            random_question = questions_formatted[0]
        elif len(questions_formatted) == 0:
            abort(404, {'message': 'no more questions in current categories'})
        else:
            random_question = questions_formatted[random.randint(0, len(questions_formatted)-1)]



        return jsonify({
            'success': True,
            'question': random_question
        })

    '''
  Done
  Create error handlers for all expected errors 
  including 400, 404, 422, and 500.
  '''

    @app.errorhandler(400)
    def bad_quest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": getErrorMessage(error, "bad request")
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": getErrorMessage(error, "resource not found")
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": getErrorMessage(error, "unprocessable")
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
