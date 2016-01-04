from flask import Blueprint, jsonify
from app.outils import utile
from app import app, db
from app.formulaires import utilisateur as fu

apibp = Blueprint('apibp', __name__, url_prefix='/api')


@apibp.route('/utilisateurs', methods=['GET'])
def api_utilisateurs():
    users = db.session.execute("SELECT * FROM utilisateurs").fetchall()

    users_dict = {}
    for a, b, c, d, e, f, g, h, i, j, k in users:
        users_dict.setdefault(a, []).append([b, c, d, e, f, g, h, i, j, k])

    utile.ecrire_json(users_dict, "app/static/data/api/utilisateurs.json")
    utilisateurs = utile.lire_json('app/static/data/api/utilisateurs.json')

    return jsonify(utilisateurs)
