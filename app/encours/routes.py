from flask import render_template, flash, url_for, redirect, request
from .. import db, bcrypt
from ..models import Encours
from app.encours.forms import EncoursForm
from flask_login import login_user, current_user, logout_user, login_required

from . import encours


#Ajouter un encours
@encours.route('/ajouterencours', methods=['GET', 'POST'])
@login_required
def ajouter_encours():

    title="Ajouter un sondage"
    #Ajouter le sondage encours
    form=EncoursForm()
    if form.validate_on_submit():
        ver_encours=Encours.query.filter_by(status=True).first() #Encours
        if ver_encours is not None:
            ver_encours.status=False
            db.session.commit()
        encours=Encours(titre=form.nom.data, status=True)
        db.session.add(encours)
        db.session.commit()
        flash('Vous avez ajouté un sondage','success')
        return redirect(url_for('encours.liste_encours'))
    return render_template('encours/ajouterrub.html', form=form, title=title)

#Liste des encours
@encours.route('/listeencours')
@login_required
def liste_encours():

    title="Liste des sondages"
     #Liste des sondages
    list_encours=Encours.query.all()

    return render_template('encours/listerub.html', title=title, encours=list_encours)


#Activation du statut du sondage
@encours.route('/sondage/<int:sondage_id>', methods=['GET','POST'])
@login_required
def status_encours(sondage_id):
    #Verification de l'existence du sondage
    encours_mo=Encours.query.filter_by(id=sondage_id).first_or_404()

    if encours_mo.status == 0:
        encours_mo.status = 1
        db.session.commit()
        flash("Le sondage est activé",'success')
        return redirect(url_for('encours.liste_encours'))
    else:
        encours_mo.status =0
        db.session.commit()
        return redirect(url_for('encours.liste_encours'))
    return render_template('rubriques/listerub.html')


#Activation du statut de ribrique
@encours.route('/editer_sondage/<int:sondage_id>', methods=['GET','POST'])
@login_required
def sondage_edit(sondage_id):

    title="Modification du sondage"
    #Verification de l'existence du sondage
    sondage=Encours.query.filter_by(id=sondage_id).first_or_404()
    if sondage is None:
        return redirect(url_for('encours.liste_encours'))
    
    #Mise à jour de la rubrique
    form=EncoursForm()
    if form.validate_on_submit():
        sondage.titre=form.nom.data
        db.session.commit()
        flash('Modification avec succès','success')
        return redirect(url_for('encours.liste_encours'))
    elif request.method == 'GET':
        form.nom.data=sondage.titre

    return render_template('encours/editerrub.html',  title=title, form=form)

    
