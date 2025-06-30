from flask import Flask, request, render_template, redirect, url_for
from data_manager import DataManager
from sqlalchemy.exc import OperationalError
from models import db, Movie, User
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #using abspath to work on from whenever you call the app.py
db_path = os.path.join(basedir, 'data', 'moviwebapp.db') #using abspath to work on from whenever you call the app.py
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.

data_manager = DataManager() # Create an object from DataManager class


@app.route('/')
def home():
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except (IOError,OperationalError) as e:
        print("An IOError occurred: ", str(e))
        error = "Sorry, we cannot load the user list right now."
        return render_template('index.html', users=[], error=error)


@app.route('/users', methods=['POST'])
def create_user():
    try:
        username = request.form.get('name')
        data_manager.create_user(username)
        return redirect(url_for('home'))
    except (IOError, OperationalError) as e:
        print("An IOError occurred: ", str(e))
        error = "Sorry, we cannot load the user list right now."
        return render_template('index.html', users=[], error=error)

@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == 'GET':
        try:
            movies = data_manager.get_movies(user_id)
            return render_template('movies.html', movies=movies, user_id=user_id)
        except IOError as e:
            print("An IOError occurred: ", str(e))

    else:
        movie_title = request.form.get('title')
        try:
            data_manager.add_movie(movie_title, user_id)
            return redirect(url_for('user_movies', user_id=user_id))
        except ValueError as e:
            error_message = str(e)
            movies = data_manager.get_movies(user_id)
            return render_template('movies.html', movies=movies, user_id=user_id, error=error_message)

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    try:
        new_movie_name = request.form.get('new_title')
        data_manager.update_movie(movie_id, new_movie_name)
        return redirect(url_for('user_movies', user_id=user_id))
    except IOError as e:
        print("An IOError occurred: ", str(e))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except IOError as e:
        print("An IOError occurred: ", str(e))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  """
  #run only if you create first time the db
  with app.app_context():
    db.create_all()
    """

  app.run(host="0.0.0.0", port=5001, debug=True)