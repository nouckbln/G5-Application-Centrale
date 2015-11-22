from flask import Flask

# Génération de l'application
app = Flask(__name__)

# Récupération des paramètres dans "config.py"
app.config.from_object('config')

# Configuration de la base de données
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Configuration de la génération de clés secrètes
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Importation des vues
from app.views import main, admin, restaurant

# Configuration des comptes utilisateurs
from flask.ext.login import LoginManager
from app.models import Restaurant

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'restaurant/connexion'


@login_manager.user_loader
def load_user(rid):
    return Restaurant.query.filter(Restaurant.rid == rid).first()
