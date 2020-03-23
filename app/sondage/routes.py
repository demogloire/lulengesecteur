from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Sondage, Encours, Choice
from app.sondage.forms import AjouterSondageForm, EditerSondageForm
from app.sondage.others_posts import save_picture, save_picture_thumb, user_mac
from flask_login import login_user, current_user, logout_user, login_required


from . import sondage

@sondage.route('/ajouter_sondage', methods=['GET', 'POST'])
@login_required
def ajouter_sondage():
    
    title="Ajouter article"
    #Formulaire d'ajout des informations sur le sondage
    form=AjouterSondageForm()
    #Envoi du formulaire des informations
    if form.validate_on_submit():
        if form.picture.data:
            #Enregistrement des infromation sur le sondage
            imagefile_thumb=save_picture_thumb(form.picture.data)
            sondage=Sondage(noms=form.noms.data.upper(), partie=form.partie.data.upper(), avatar=imagefile_thumb, encours_sondage=form.encours.data)
            db.session.add(sondage)
            db.session.commit()
            flash('Ajouter avec succès','success')
            return redirect(url_for('sondage.ajouter_sondage'))        
    return render_template('sondage/ajouter.html', title=title, form=form)


@sondage.route('/listesondage')
@login_required
def tous_sondage():
    title='Liste des sondages'
    list_encours=Encours.query.all()
    return render_template('sondage/sondage.html', title=title, encours=list_encours)


@sondage.route('/sondage/<int:sondage_id>/realise')
@login_required
def sondage_passe(sondage_id):
    title='Liste des sondages'
    list_encours=Encours.query.filter_by(id=sondage_id).first()
    nom_sondage=list_encours.titre
    sondage=Sondage.query.filter_by(encours_id=sondage_id).all()
    return render_template('sondage/sangae_passe.html', title=title, sondage=sondage, nom=nom_sondage)


@sondage.route('/editer_sondage_condidat/<int:sondage_id>', methods=['GET', 'POST'])
@login_required
def sondage_edit_candidat(sondage_id):

    form=EditerSondageForm()
    sondage=Sondage.query.filter_by(id=sondage_id).first_or_404()
    if form.validate_on_submit():
        if form.picture.data:
            image=save_picture_thumb(form.picture.data)
            sondage.noms=form.noms.data.upper()
            sondage.partie=form.partie.data.upper() 
            sondage.avatar=image
            encours_sondage=form.encours.data
            db.session.commit()
            flash("Les informations modifiée",'success')
            return redirect(url_for('sondage.sondage_passe', sondage_id=sondage.encours_id ))
        sondage.noms=form.noms.data.upper()
        sondage.partie=form.partie.data.upper() 
        encours_sondage=form.encours.data
        db.session.commit()
        flash("Les informations modifiée",'success')
        return redirect(url_for('sondage.sondage_passe', sondage_id=sondage.encours_id ))
    elif request.method =='GET':
        form.noms.data=sondage.noms
        form.partie.data=sondage.partie
        form.encours.data=sondage.encours_sondage  
    return render_template('sondage/edit_sondage.html', form=form)

#Page de vote
@sondage.route('/vote/<int:vote_id>', methods=['GET'])
def vote(vote_id):
    adresse=user_mac() #Mac adresse
    candidat_sondage=vote_id #Vote candidant
    #vérification d'election
    ver_election=Choice.query.filter_by(sondage_id=candidat_sondage, visiteur_id=adresse).first()
    sondage=Sondage.query.filter_by(id=vote_id).first()
    if ver_election is not None:
        return redirect(url_for('main.homepage'))
    else:
        choix=Choice(sondage_id=candidat_sondage, visiteur_id=adresse)
        sondage.compteur= sondage + 1
        db.session.add(choix)
        db.session.commit()
        return redirect(url_for('main.homepage'))


    return render_template('user/vote.html')









