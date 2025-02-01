# makes this website folder a python package
# means that we can import this folder and whatever is inside this file will run automatically

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from os import path

# db = SQLAlchemy()
# DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__) # __name__ represents the name of the file that was ran, basically how you initialise flask
    app.config['SECRET_KEY'] = 'dsfdsfsdfsddfg'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # sqlalchemy database is located at database.db in website folder
    # db.init_app(app) # initialise database (this is the database we are going to use)

    from .views import views #relative import

    # url prefix: your route in the @smth.route() is prefixed by whatever you define as the url prefix
    app.register_blueprint(views, url_prefix='/')

    # from .models import Note

    #create_database(app)
    
    return app
