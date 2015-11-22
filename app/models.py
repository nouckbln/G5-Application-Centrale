from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin


class Restaurant(db.Model, UserMixin):
    __tablename__ = 'restaurants'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String)
    adresse = db.Column(db.String)
    capacite = db.Column(db.Integer)
    mdp = db.Column(db.String)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    @hybrid_property
    def password(self):
        return self.mdp

    @password.setter
    def _set_mdp(self, plaintext):
        self.mdp = bcrypt.generate_password_hash(plaintext)

    def verifier_mdp(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        return self.rid


class Reservation(db.Model):
    __tablename__ = 'reservations'
    __table_args__ = (
        db.PrimaryKeyConstraint('rid', 'nom', 'date'),
    )
    rid = db.Column(
        db.Integer, db.ForeignKey('restaurants.rid'), autoincrement=False)
    nom = db.Column(db.String)
    places = db.Column(db.Integer)
    date = db.Column(db.Date)
    heure = db.Column(db.Integer)
    tel = db.Column(db.Integer)


class Ouverture(db.Model):
    __tablename__ = 'ouvertures'
    __table_args__ = (
        db.PrimaryKeyConstraint('rid', 'jour'),
    )
    rid = db.Column(
        db.Integer, db.ForeignKey('restaurants.rid'), autoincrement=False)
    jour = db.Column(db.Integer)
    debut = db.Column(db.String)
    fin = db.Column(db.String)
