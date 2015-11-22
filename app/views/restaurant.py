from flask import render_template, redirect, url_for, abort
from app import app
from app import forms
from app import models


@app.route('/restaurant/connecter', methods=['GET', 'POST'])
def restaurant_connecter():
    form = forms.Connexion()
    if form.validate_on_submit():
        utilisateur = models.Utilisateur.query.filter_by(
            email=form.email.data).first()
        if requete.verifier_connexion(utilisateur):
            login_user(utilisateur)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('connecter'))
    return render_template('restaurant/connecter.html', form=form)


@app.route('/restaurant/deconnecter')
def restaurant_deconnecter():
    logout_user()
    return redirect(url_for('index'))
