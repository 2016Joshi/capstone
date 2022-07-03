from crypt import methods
from datetime import datetime
import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from models import Actor, setup_db, Movie, db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # setup CORS
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Casting agency home'
        })

    '''Movies endpoints'''

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
        }), 200

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        else:
            return jsonify({
              'success': True,
              'movie': movie.format(),
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        if title is None or release_date is None:
            abort(400)
        release_date = datetime.strptime(release_date, '%Y/%m/%d')
        movie = Movie(title=title, release_date=release_date)
        try:
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 201
        except Exception:
            abort(500)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200
        except Exception:
            abort(500)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        try:
            movie.delete()
            return jsonify({
                'success': True,
                'message':
                f'movie id {movie.id}, titled {movie.title} is deleted',
            }), 200
        except Exception:
            db.session.roleback()
            abort(500)

    '''Actor endpoints'''

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
        }), 200

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(jwt, id):

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        if name is None or age is None or gender is None:
            abort(400)

        actor = Actor(name=name, age=age, gender=gender)
        try:
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 201
        except Exception:
            abort(500)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        if name is None or age is None or gender is None:
            abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200
        except Exception:
            abort(500)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):

        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'message':
                f'actor id {actor.id}, named {actor.name} is deleted',
            }), 200
        except Exception:
            db.session.roleback()
            abort(500)

    '''error handling'''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
