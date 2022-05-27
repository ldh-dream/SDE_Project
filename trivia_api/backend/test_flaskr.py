import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    ##############GET on /categories##################
    def test_get_all_categories(self):
        """get all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    #########DELET question /questions/<int:question_id> ###
    # def test_delete_question_by_id(self):
    #     """delete questions"""
    #     last_question_id = Question.query.order_by(desc(Question.id)).first().id
    #     res = self.client().delete('/questions/{}'.format(last_question_id))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], last_question_id)

    def test_error_400_delete_nonexist_questiono_by_id(self):
        """delete a question which id is not existed"""
        res = self.client().delete('/questions/123456')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)



    ################Test for the ./questions#############
    def test_get_paginated_questions(self):
        """
        test GET ./questions
        """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_error_405_paginated_questions(self):
        """
        un-allowed method on '/questions'
        """
        res = self.client().patch('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")

    #########POST ./question################
    def test_error_404_search_question(self):
        """ non existing search term. """

        # Used as header to POST /question
        json_search_question = {
            'searchTerm': 'no such stuff in search',
        }

        res = self.client().post('/questions', json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'no questions which contains no such stuff in search found.')

    def test_search_question(self):
        json_search_question = {
            'search': 'which',
        }
        res = self.client().post('/questions', json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    ######Get /categories/<int:category_id>/questions'########
    def test_get_questions_by_category_id(self):
        def test_get_questions_from_category(self):
            """Test GET all questions from selected category."""
            res = self.client().get('/categories/1/questions')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(len(data['questions']))
            self.assertTrue(data['total_questions'])
            self.assertEqual(data['current_category'], '1')

    def test_400_get_questions_by_category_id(self):
        """Test 400 if no questions with queried category is available."""
        res = self.client().get('/categories/1234567/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'id 1234567 category does not exists')
################play quiz#######################
    def test_error_400_play_quiz(self):
        """Test /quiz error without any request"""
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'request not found')

    def test_error_404_play_quiz(self):
        """Test /quiz error without any request"""
        res = self.client().post('/quizzzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_play_quiz_with_category(self):
        """Test /quiz succesfully with given category """
        json_play_quizz = {
            'previous_questions': [1],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }
        res = self.client().post('/quizzes', json=json_play_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['question'])
        # Also check if returned question is NOT in previous question
        self.assertTrue(data['question']['id'] not in json_play_quizz['previous_questions'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
