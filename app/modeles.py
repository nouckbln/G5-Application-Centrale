from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin


class Utilisateur(db.Model, UserMixin):

    ''' Un utilisateur du site web. '''

    __tablename__ = 'utilisateurs'
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    numero = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _mdp = db.Column(db.String)

    @hybrid_property
    def mdp(self):
        return self._mdp

    @mdp.setter
    def _set_password(self, plaintext):
        self._mdp = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.mdp, plaintext)

    def get_id(self):
        return self.email
