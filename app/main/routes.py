import os
from flask import render_template, make_response, flash, url_for, redirect, request, session
from ..models import Contenu, Photo, Album, Sondage, Encours
import pdfkit
from . import main


@main.route('/')
def homepage():
    posts=Contenu.query.filter_by(status=True).order_by(Contenu.date_p.desc()).limit(3) #Contenue
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    id_album=album.id
    
    if album is not None:
        photos=Photo.query.filter_by(album_id=id_album).limit(6) #Photo
        ver_album='Novide'
    
    encours=Encours.query.filter_by(status=True).order_by(Encours.id.desc()).first() #Sondage en cours
    ver_encours="Vide"
    candidat=None
    if encours is not None:
        ver_encours="NoVide"
        candidat=Sondage.query.filter_by(encours_id=encours.id).limit(4)
        candidat_totale=Sondage.query.filter_by(encours_id=encours.id).all()
        table_par_sondage=[] #Tableau valeur vendue
        for somme in candidat_totale:
            i=somme.id
            table_par_sondage.insert(0,i)
        total_sondage=len(table_par_sondage)
    pourcentage=total_sondage/100
    sondage_nom=encours.titre

    return render_template('main/homepage.html', pourcentage=pourcentage, total_sondage=total_sondage, title="Secteur lulenge fizi", sondage_nom=sondage_nom, ver_encours=ver_encours,candidat=candidat,photos=photos, post=posts, ver_album=ver_album)



@main.route('/apropos_de_nous.html')
def apropos_de_nous():
 
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
   
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    
    return render_template('main/apropos.html',  title="Apropos de nous", photos=photos, ver_album=ver_album)


@main.route('/sondage.html')
def sondage_vue():

    title="Sondage"
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    
    #Le sondage actif
    encours=Encours.query.filter_by(status=True).order_by(Encours.id.desc()).first() #Sondage en cours
    ver_encours="Vide"
    candidat=None
    page= request.args.get('page', 1, type=int)  #Pagination de 50 candidature

    #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours

    if encours is not None:
        ver_encours="NoVide"
        candidat=Sondage.query.filter_by(encours_id=encours.id).order_by(Sondage.compteur.desc()).paginate(page=page, per_page=50)
        candidat_totale=Sondage.query.filter_by(encours_id=encours.id).all()
        table_par_sondage=[] #Tableau valeur vendue
        for somme in candidat_totale:
            i=somme.id
            table_par_sondage.insert(0,i)
        total_sondage=len(table_par_sondage)
    pourcentage=total_sondage/100
    sondage_nom=encours.titre

    return render_template('main/sondage.html',encours_rapport=encours_rapport,candidat=candidat,total_sondage=total_sondage, ver_encours=ver_encours,sondage_nom=sondage_nom, title=title, photos=photos, ver_album=ver_album)



@main.route('/sondage_rapport/<int:sond_id>')
def sondage_rapport(sond_id):
    encours=Encours.query.filter_by(id=sond_id).order_by(Encours.id.desc()).first_or_404()
    candidat=Sondage.query.filter_by(encours_id=encours.id).order_by(Sondage.compteur.desc())
    rendered=render_template('main/rapport_sondage.html', candidat=candidat, sondage_nom=encours.titre)
    pdf= pdfkit.from_string(rendered, False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=rapport.pdf'





