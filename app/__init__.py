from flask import Flask

app = Flask(__name__)

# Générer l'application avec les options du fichier config.py
app.config.from_object('config')

# Se connecter à la base de données
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Mettre en place le serveur email
from flask.ext.mail import Mail
mail = Mail(app)

# Mettre en place l'outil pour générer des clés secrètes
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Importer les vues
from app.vues import principal, utilisateur, erreur
app.register_blueprint(utilisateur.utilisateurbp)

# Mettre en place la gestion de compte utilisateur
from flask.ext.login import LoginManager
from app.modeles import Utilisateur

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'utilisateurbp.connexion'


@login_manager.user_loader
def load_user(email):
    return Utilisateur.query.filter(Utilisateur.email == email).first()

# Ajouter une interface administrateur
from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import LoginManager
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op

admin = Admin(app, name='Admin', template_mode='bootstrap3')

class VueModele(ModelView):

    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('Il faut rentrer les identifiants administrateur.', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True

# Utilisateurs
admin.add_view(VueModele(Utilisateur, db.session))
# Fichiers statiques
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static'))