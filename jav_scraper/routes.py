from flask import jsonify

from . import app
from . import models


@app.route('/movies', methods=['GET'])
def get_movies():
    movies = []
    for movie in models.JAVMovie.query.all():
        movie = movie.__dict__.copy()
        movie.pop('_sa_instance_state', None)
        movies.append(movie)

    return jsonify(movies)

@app.route('/grabs', methods=['GET'])
def get_grabs():
    grabs = []
    for grab in models.Grab.query.all():
        grab = grab.__dict__.copy()
        grab.pop('_sa_instance_state', None)
        grabs.append(grab)

    return jsonify(grab)
