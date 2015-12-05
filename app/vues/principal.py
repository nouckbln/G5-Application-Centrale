from flask import render_template, jsonify
from app import app
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Accueil')


@app.route('/carte')
def carte():
    return render_template('carte.html', titre='Carte')


@app.route('/rafraichir_carte', methods=['POST'])
def rafraichir_carte():
    lat = random.uniform(48.8434100, 48.8634100)
    lon = random.uniform(2.3388000, 2.3588000)
    return jsonify({'position': [lat, lon]})


@app.route('/informations')
def informations():
    return render_template('informations.html', titre='Informations')


@app.route('/contact')
def contact():
    return render_template('contact.html', titre='Contact')
