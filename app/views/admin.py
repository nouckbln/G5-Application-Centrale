from flask import render_template, redirect, url_for, request
from itsdangerous import URLSafeTimedSerializer
from app import app
from app import forms
from app import models
from app import db

# Sérialiseur pour générer un token dans un mail
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/connecter.html')


@app.route('/admin/connecter', methods=['GET', 'POST'])
def admin_connecter():
    mdp = request.form.get('mdp')
    if mdp == app.config['SECRET_KEY']:
        return redirect(url_for('admin_restaurants', connected=True))
    return redirect(url_for('admin'))


@app.route('/admin/ajouter', methods=['POST'])
def admin_ajouter():
    form = forms.EnregistrementRestaurant(request.form)
    if form.validate_on_submit():
        restaurant = models.Restaurant(
            nom=form.nom.data,
            adresse=form.adresse.data,
            capacite=int(form.capacite.data),
            mdp=form.mdp.data,
            lat=float(form.lat.data),
            lon=float(form.lon.data)
        )
        db.session.add(restaurant)

        lundi = models.Ouverture(
            rid=form.nom.data,
            jour=1,
            debut=form.o1.data,
            fin=form.f1.data
        )
        db.session.add(lundi)

        mardi = models.Ouverture(
            rid=form.nom.data,
            jour=2,
            debut=form.o2.data,
            fin=form.f2.data
        )
        db.session.add(mardi)

        mercredi = models.Ouverture(
            rid=form.nom.data,
            jour=3,
            debut=form.o3.data,
            fin=form.o3.data
        )
        db.session.add(mercredi)

        jeudi = models.Ouverture(
            rid=form.nom.data,
            jour=4,
            debut=form.o4.data,
            fin=form.o4.data
        )
        db.session.add(jeudi)

        vendredi = models.Ouverture(
            rid=form.nom.data,
            jour=5,
            debut=form.o5.data,
            fin=form.f5.data
        )
        db.session.add(vendredi)

        samedi = models.Ouverture(
            rid=form.nom.data,
            jour=6,
            debut=form.o6.data,
            fin=form.f6.data
        )
        db.session.add(samedi)

        dimanche = models.Ouverture(
            rid=form.nom.data,
            jour=7,
            debut=form.o7.data,
            fin=form.f7.data
        )
        db.session.add(dimanche)

        db.session.commit()

    return redirect(url_for('admin_restaurants', connected=True))


@app.route('/admin/restaurants', methods=['GET', 'POST'])
def admin_restaurants(connected=True):
    restaurants = models.Restaurant.query.all()
    return render_template('admin/restaurants.html', connected=connected,
                           restaurants=restaurants)
