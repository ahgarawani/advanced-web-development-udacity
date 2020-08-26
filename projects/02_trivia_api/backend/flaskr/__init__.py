import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_items(request, selection):
    # return a list of paginated questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # set Access-Control-Allow using the after_request decorator
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # retrieve all existing categories in the database
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    # retrieve all existing questions, 10 questions per page
    @app.route('/questions')
    def get_questions_paginated():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_items(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })

    # delete a question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id)\
                            .one_or_none()

            if question is None:
                abort(404)

            question.delete()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_items(request, selection)

            categories = Category.query.order_by(Category.type).all()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': {category.id: category.type for category in categories},
                'current_category': None
            })

        except:
            abort(422)

    # add a new question
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question_string = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        if not (question_string and answer and difficulty and category): abort(422) 

        try:
            new_question = Question(
                question=question_string,
                answer=answer,
                difficulty=difficulty,
                category=category
            )

            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    # search for a question
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm', None)
        if search:
            selection = Question.query\
                            .filter(Question.question.ilike(f'%{search}%'))\
                            .order_by(Question.id).all()
            current_questions = paginate_items(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': None
            })
        else:
            abort(404)

    # retrieve all questions in a given category
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        selection = Question.query.filter(Question.category == category_id)\
                        .order_by(Question.id).all()
        current_questions = paginate_items(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': category_id
        })

    # play the trivia game
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        try:
            remaining_questions = Question.query\
                .filter(Question.category == quiz_category['id'] if quiz_category['id'] != 0 else not quiz_category['id'])\
                .filter(Question.id.notin_((previous_questions))).all()
            new_question = Question.query\
                .get(random.choice(remaining_questions).id)\
                .format() if len(remaining_questions) > 0 else None
            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
