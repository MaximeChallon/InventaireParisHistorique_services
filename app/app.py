from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .constantes import SECRET_KEY, SQLALCHEMY_DATABASE_URI
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__
)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = SECRET_KEY


from .routes import generals
