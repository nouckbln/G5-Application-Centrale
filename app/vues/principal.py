from flask import render_template, jsonify
from app import app
from app import db
import random
from app.outils import utile


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titre='Réserver un taxi')


@app.route('/carte')
def carte():
    return render_template('carte.html', titre='Carte')


@app.route('/rafraichir_carte', methods=['POST'])
def rafraichir_carte():
    lat = random.uniform(48.8434100, 48.8634100)
    lon = random.uniform(2.3388000, 2.3588000)
    return jsonify({'position': [lat, lon]})


@app.route('/tarifs')
def tarifs():
    return render_template('tarifs.html', titre='Tarifs')


@app.route('/informations')
def informations():
    return render_template('informations.html', titre='Informations')


@app.route('/FAQ')
def faq():
    faq_data = utile.lire_json('app/static/data/faq.json')
    return render_template('faq.html', titre='FAQ', faq_data=faq_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', titre='Contact')


@app.route('/api')
def api():
    return render_template('api.html', titre='API')
