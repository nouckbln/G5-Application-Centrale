from flask.ext.mail import Message
from app import app, mail


def envoyer(destinataire, sujet, corps):
    '''
    Envoyer un mail à une adresse email. Le corps du message est normalement
    du HTML généré à partir de Flask. Les coordonnées de l'expediteur sont
    précisées dans le fichier config.py.
    '''
    expediteur = app.config['ADMINS'][0]
    message = Message(sujet, sender=expediteur, recipients=[destinataire])
    message.html = corps
    with app.app_context():
        mail.send(message)
