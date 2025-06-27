import requests
from models import db, User, Movie
import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

class DataManager:
    # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return User.query.all()

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id = user_id).all()

    def add_movie(self, title, user_id):
        response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}')
        data = response.json()

        if data['Response'] == 'True':
            new_movie = Movie(
                name = data["Title"],
                director = data["Director"],
                year = int(data["Year"]),
                poster_url = data["Poster"],
                user_id=user_id
            )

            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        else:
            raise ValueError('Movie not found in OMDb')

    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return movie
        else:
            raise ValueError(f"Movie with ID {movie_id} not found.")

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return f"Movie '{movie.name}' deleted successfully."
        else:
            raise ValueError(f"Movie with ID {movie_id} not found.")
