from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required,  ValidationError
from app.models import Restaurant


class ConnexionRestaurant(Form):

    ''' Formulaire pour qu'un restaurant se connecte. '''

    nom = TextField('Nom du restaurant', [Required()])
    mdp = PasswordField('Mot de passe', [Required()])


class EnregistrementRestaurant(Form):

    ''' Formulaire pour enregistrer un restaurant. '''

    nom = TextField('Nom', [Required()])
    adresse = TextField('Adresse', [Required()])
    capacite = TextField('Capacité', [Required()])
    mdp = PasswordField('Mot de passe', [Required()])
    lat = TextField('Latitude', [Required()])
    lon = TextField('Latitude', [Required()])
    o1 = TextField('Ouverture lundi', [Required()])
    f1 = TextField('Fermeture lundi', [Required()])
    o2 = TextField('Ouverture mardi', [Required()])
    f2 = TextField('Fermeture mardi', [Required()])
    o3 = TextField('Ouverture mercredi', [Required()])
    f3 = TextField('Fermeture mercredi', [Required()])
    o4 = TextField('Ouverture jeudi', [Required()])
    f4 = TextField('Fermeture jeudi', [Required()])
    o5 = TextField('Ouverture vendredi', [Required()])
    f5 = TextField('Fermeture vendredi', [Required()])
    o6 = TextField('Ouverture samedi', [Required()])
    f6 = TextField('Fermeture samedi', [Required()])
    o7 = TextField('Ouverture dimanche', [Required()])
    f7 = TextField('Fermeture dimanche', [Required()])

    def validate_on_submit(self):
        return True


class RechercherRestaurant(Form):

    ''' Formulaire pour chercher un restaurant. '''

    date = TextField('Date', [Required()])
    heure = TextField('Heures', [Required()])
    places = TextField('Places', [Required()])
