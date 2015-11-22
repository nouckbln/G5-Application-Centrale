from flask import render_template, jsonify, request
from sqlalchemy.sql import func
import json
import time
from datetime import datetime
from app import app
from app import forms
from app import models
from app import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Accueil')


def filtrer(restaurants, demande):
    candidats = []
    print(datetime.strptime(demande['date'], '%d %b %y'))
    for restaurant in restaurants:

        # Combien de places réservées ce jour ci?
        count_reservations = db.session.query(
            func.sum(models.Reservation.places.label('sum'))).filter(
            models.Reservation.rid == restaurant.rid).filter(
            int(demande['heure'])-0.5 < models.Reservation.heure).filter(
            models.Reservation.heure < int(demande['heure'])+0.5).filter(
            models.Reservation.date == datetime.strptime(
                demande['date'], '%d %b %y').date()).first()[0]

        count_reservations = count_reservations or 0

        places = restaurant.capacite - \
            count_reservations - int(demande['personnes'])

        print(places, restaurant.capacite,
              count_reservations, int(demande['personnes']))

        if places >= 0:  # demande['places']:
            candidats.append({
                'rid': restaurant.rid,
                'nom': restaurant.nom,
                'adresse': restaurant.adresse,
                'places': restaurant.capacite,
                'lat': restaurant.lat,
                'lon': restaurant.lon
            })
    return candidats


@app.route('/rechercher', methods=('GET', 'POST'))
def rechercher():
    data = json.loads(request.data.decode())
    restaurants = models.Restaurant.query.all()
    candidats = filtrer(restaurants, data)
    return jsonify({'restaurants': candidats})


@app.route('/reserver', methods=('GET', 'POST'))
def reserver():
    data = json.loads(request.data.decode())
    reservation = models.Reservation(
        rid=int(data['rid']),
        date=datetime.strptime(data['date'], '%d %b %y'),
        heure=int(data['heure']),
        places=int(data['personnes']),
        nom=data['nom'],
        tel=int(data['tel'])
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation effectuée!'})


@app.route('/informations')
def informations():
    return render_template('informations.html', title='Informations')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
