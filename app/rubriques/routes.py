from flask import render_template, flash, url_for, redirect, request
from .. import db, bcrypt
from ..models import Rubrique
from app.rubriques.forms import RubriqueForm, EditerRubriqueForm
from flask_login import login_user, current_user, logout_user, login_required

from . import rubriques


#Ajouter une nouvelle rubrique dans le systeme
@rubriques.route('/ajouter_rubrique', methods=['GET', 'POST'])
@login_required
def ajouter_rubrique():

    title="Ajouter rubrique"
    #Ajouter de la rubrique
    form=RubriqueForm()
    if form.validate_on_submit():
        rub=Rubrique(nom=form.nom_rub.data, status=0)
        db.session.add(rub)
        db.session.commit()
        flash('Ajout de rubrique avec succès','success')
        return redirect(url_for('rubriques.liste_rubrique'))
    return render_template('rubriques/ajouterrub.html', form=form, title=title)

#Liste des rubiruque du systeme
@rubriques.route('/liste_rubrique')
@login_required
def liste_rubrique():

    title="Liste des rubriques"
     #Liste des rubriques
    list_rub=Rubrique.query.all()

    return render_template('rubriques/listerub.html', title=title, rub=list_rub)


#Activation du statut de ribrique
@rubriques.route('/status/<int:rub_id>', methods=['GET','POST'])
@login_required
def status_rub(rub_id):
    #Verification de l'existence de Rubirque
    rub_mo=Rubrique.query.filter_by(id=rub_id).first_or_404()
    if rub_mo is None:
        flash("Veuillez respecté la procedure",'danger')
        return redirect(url_for('rubriques.liste_rubrique'))
    else:#Changement du statut
        if rub_mo.status == 1:
            rub_mo.status = 0
            db.session.commit()
            flash("La rubrique est désactivée sur la plateforme",'success')
            return redirect(url_for('rubriques.liste_rubrique'))
        elif rub_mo.status == 0:
            rub_mo.status = 1
            db.session.commit()
            flash("La rubrique est activée sur la plateforme",'success')
            return redirect(url_for('rubriques.liste_rubrique'))

    return render_template('rubriques/listerub.html')


#Activation du statut de ribrique
@rubriques.route('/editer_user/<int:rub_id>', methods=['GET','POST'])
@login_required
def editer_user(rub_id):

    title="Modification de la rubrique"
    #Verification de l'existence de rubrique
    rubriques=Rubrique.query.filter_by(id=rub_id).first_or_404()
    if rubriques is None:
        return redirect(url_for('users.dashboard'))
    
    #Mise à jour de la rubrique
    form=EditerRubriqueForm()
    if form.validate_on_submit():
        rubriques.nom=form.nomedrub.data
        db.session.commit()
        return redirect(url_for('rubriques.liste_rubrique'))
    elif request.method == 'GET':
        form.nomedrub.data=rubriques.nom

    return render_template('rubriques/editerrub.html',  title=title, form=form)

    
