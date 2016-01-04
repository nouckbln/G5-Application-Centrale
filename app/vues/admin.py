from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op
from app import app
from app import admin
from app import modeles
from app import db


class VueModele(ModelView):
    '''
    Vue de base qui implémente une authentification
    HTTP. Toutes les autres vues héritent de cette vue.
    '''

    def is_accessible(self):
        auth = request.authorization or request.environ.get(
            'REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('Il faut rentrer les identifiants administrateur.', 401,
                                             {'WWW-Authenticate': 'Basic realm="Identifiants requis"'}
                                             ))
        return True


class VueUtilisateur(VueModele):

    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = False
    can_delete = False

    # Colonnes invisible
    column_exclude_list = ['_mdp']

    # Colonnes pour chercher
    column_searchable_list = ['prenom', 'nom']

    # Colonnes pour filtrer
    column_filters = ['categorie', 'inscription', 'confirmation']


# Utilisateurs
admin.add_view(VueUtilisateur(modeles.Utilisateur, db.session))
# Fichiers de style
path = op.join('/'.join(op.dirname(__file__).split('/')[:-1]), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static'))
