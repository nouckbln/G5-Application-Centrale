from flask import (Blueprint, render_template, redirect, url_for,
                   abort, flash)
from flask.ext.login import login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from app import app, modeles, db
from app.formulaires import utilisateur as fu
from app.outils import email

# Serialiseur pour générer des tokens aléatoires
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Créer un patron pour les vues utilisateurs
utilisateurbp = Blueprint('utilisateurbp', __name__, url_prefix='/utilisateur')


@utilisateurbp.route('/enregistrement', methods=['GET', 'POST'])
def enregistrement():
    form = fu.Enregistrement()
    if form.validate_on_submit():
        # Créer un utilisateur qui n'a pas confirmé son mail
        utilisateur = modeles.Utilisateur(
            prenom=form.prenom.data,
            nom=form.nom.data,
            numero=form.numero.data,
            email=form.email.data,
            confirmation=False,
            mdp=form.mdp.data,
        )
        # Insérer un utilisateur dans la BD
        db.session.add(utilisateur)
        db.session.commit()
        # Sujet du mail à envoyer
        sujet = 'Veuillez confirmer votre adresse email.'
        # Générer un token aléatoire
        token = ts.dumps(utilisateur.email, salt='email-confirm-key')
        # Construire un lien de confirmation à partir du token
        urlConfirmation = url_for('utilisateurbp.confirmation',
                                  token=token, _external=True)
        # Le corps du mail est un template écrit en HTML
        html = render_template('email/confirmation.html',
                               url_confirmation=urlConfirmation)
        # Envoyer le mail à l'utilisateur
        email.envoyer(utilisateur.email, sujet, html)
        # On renvoit à la page d'accueil
        flash('Vérifiez vos mails pour confirmer votre adresse email.',
              'positive')
        return redirect(url_for('index'))
    return render_template('utilisateur/enregistrement.html',
                           form=form, titre='Enregistrement')


@utilisateurbp.route('/confirmation/<token>', methods=['GET', 'POST'])
def confirmation(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    # Le token peut avoir expiré ou être invalide
    except:
        abort(404)
    # Récupérer l'utilisateur de la BD
    utilisateur = modeles.Utilisateur.query.filter_by(email=email).first()
    # L'utilisateur a maintenant confirmé son mail
    utilisateur.confirmation = True
    # On met à jour la BD
    db.session.commit()
    # On renvoit à la page de connexion
    flash('Votre adresse email a été confirmé, vous pouvez maintenant ' +
          'vous connecter.', 'positive')
    return redirect(url_for('utilisateurbp.connexion'))


@utilisateurbp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = fu.Connexion()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(
            email=form.email.data).first()
        # On vérifie que l'utilisateur existe
        print(utilisateur.mdp)
        if utilisateur is not None:
            # On vérifie ensuite que le mot de passe est correct
            if utilisateur.check_password(form.mdp.data):
                login_user(utilisateur)
                # On renvoit à la page d'accueil
                flash('Vous vous êtes connecté avec succès.', 'positive')
                return redirect(url_for('index'))
            else:
                flash('Vous avez rentré un mot de passe invalide.', 'negative')
                return redirect(url_for('utilisateurbp.connexion'))
        else:
            flash("Vous avez rentré une adresse email qui n'est pas associé " +
                  'à un compte.', 'negative')
            return redirect(url_for('utilisateurbp.connexion'))
    return render_template('utilisateur/connexion.html', form=form,
                           titre='Connexion')


@utilisateurbp.route('/deconnexion')
def deconnexion():
    logout_user()
    flash('Vous vous êtes déconnecté avec succès.', 'positive')
    return redirect(url_for('index'))


@utilisateurbp.route('/compte')
@login_required
def compte():
    return render_template('utilisateur/compte.html', titre='Compte')


@utilisateurbp.route('/oubli', methods=['GET', 'POST'])
def oubli():
    form = fu.Oubli()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(
            email=form.email.data).first()
        # On vérifie que l'utilisateur existe
        if utilisateur is not None:
            # Sujet du mail de confirmation
            sujet = 'Veuillez réinitialiser votre mot de passe.'
            # Générer un token aléatoire
            token = ts.dumps(utilisateur.email, salt='password-reset-key')
            # Construire un lien de réinitialisation à partir du token
            urlReinitialisation = url_for('utilisateurbp.reinitialisation',
                                          token=token, _external=True)
            # Le corps du mail est un template écrit en HTML
            html = render_template('email/reinitialisation.html',
                                   url_reinitialisation=urlReinitialisation)
            # Envoyer le mail à l'utilisateur
            email.envoyer(utilisateur.email, sujet, html)
            # On renvoit à la page d'accueil
            flash('Vérifiez vos mail pour réinitialiser votre mot de passe.',
                  'positive')
            return redirect(url_for('index'))
        else:
            flash("Vous avez rentré une adresse email qui n'est pas associé " +
                  'à un compte.', 'negative')
            return redirect(url_for('utilisateurbp.oubli'))
    return render_template('utilisateur/oubli.html', form=form)


@utilisateurbp.route('/reinitialisation/<token>', methods=['GET', 'POST'])
def reinitialisation(token):
    try:
        email = ts.loads(token, salt='password-reset-key', max_age=86400)
    # Le token peut avoir expiré ou être invalide
    except:
        abort(404)
    form = fu.Reinitialisation()
    if form.validate_on_submit():
        utilisateur = modeles.Utilisateur.query.filter_by(email=email).first()
        # On vérifie que l'utilisateur existe
        if utilisateur is not None:
            utilisateur.mdp = form.mdp.data
            # On met à jour la BD
            db.session.commit()
            # On renvoit à la page de connexion
            flash('Votre mot de passe a été mis à jour, vous pouvez ' +
                  'maintenant vous connecter.', 'positive')
            return redirect(url_for('utilisateurbp.connexion'))
        else:
            flash("Vous avez rentré une adresse email qui n'est pas associé " +
                  'à un compte.', 'negative')
            return redirect(url_for('utilisateurbp.oubli'))
    return render_template('utilisateur/reinitialisation.html',
                           form=form, token=token)
