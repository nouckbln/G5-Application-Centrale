import random
import unittest
import sure

from app import app
from app import db


# Ajouter les classes de test pour l'application Flask

# Ensemble des classes de tests concernant la BD
class TestBD(unittest.TestCase):

    def set_up_db(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:houdini@localhost/taxisid'
        self.app = app.test_client()
        db.create_all()

    def tear_down_db(self):
        db.session.remove()
        db.drop_all()

#    def test_insert(self):

#    def test_delete(self):

#    def test_update(self):
