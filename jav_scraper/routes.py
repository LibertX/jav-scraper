from flask import jsonify, request

from . import app
from . import db
from . import models


@app.route('/movies', methods=['GET'])
def get_movies():
    movies = []
    for movie in models.JAVMovie.query.all():
        movie = movie.__dict__.copy()
        movie.pop('_sa_instance_state', None)
        movies.append(movie)

    return jsonify(movies)


@app.route('/movies', methods=['POST'])
def add_movie():
    if models.JAVMovie.query.filter_by(code=request.json['code']).first():
        return '', 409
    movie = models.JAVMovie()
    movie.code = request.json['code']
    movie.status = 'pending'
    db.session.add(movie)
    db.session.commit()
    return '', 204


@app.route('/movie/<code>', methods=['DELETE'])
def remove_movie(code):
    movie = models.JAVMovie.query.filter_by(code=code).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    return '', 204


@app.route('/grabs', methods=['GET'])
def get_grabs():
    grabs = []
    for grab in models.Grab.query.all():
        grab = grab.__dict__.copy()
        grab.pop('_sa_instance_state', None)
        grabs.append(grab)

    return jsonify(grab)
