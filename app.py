from flask import Flask
from data_manager import DataManager
from models import db, Movie
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
    return "Welcome to MoviWeb App!"

if __name__ == '__main__':
  """
  #run only if you create first time the db
  with app.app_context():
    db.create_all()
    """
  app.run(host="0.0.0.0", port=5001, debug=True)