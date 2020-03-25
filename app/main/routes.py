import os
from flask import render_template, make_response, flash, url_for, redirect, request, session
from ..models import Contenu, Photo, Album, Sondage, Encours, Rubrique, Like, Commentaire, Comment
from .. import db
from app.main.forms import CommentaireUnForm
from app.main.others_posts import save_picture, save_picture_thumb, user_mac, ver_enre_article, ver_enre_lu, lesvisteurs 
from flask_login import login_user, current_user, logout_user, login_required 
import pdfkit
from . import main


@main.route('/')
def homepage():

    #Les posts publies
    posts=Contenu.query.filter_by(status=True).order_by(Contenu.date_p.desc()).limit(3) #Contenue
    ver_post_active="Vide"
    if posts is not None:
        ver_post_active="NoVide"

    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    id_album=album.id
    lesvisteurs() #Visiteur compteur
    session.pop('ver', None) # 
    session.pop('id_pu', None) #
    
    if album is not None:
        photos=Photo.query.filter_by(album_id=id_album).limit(6) #Photo
        ver_album='Novide'
    
    encours=Encours.query.filter_by(status=True).order_by(Encours.id.desc()).first() #Sondage en cours
    ver_encours="Vide"
    candidat=None
    total_sondage=0
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

    return render_template('main/homepage.html',ver_post_active=ver_post_active, pourcentage=pourcentage, total_sondage=total_sondage, title="Secteur lulenge fizi", sondage_nom=sondage_nom, ver_encours=ver_encours,candidat=candidat,photos=photos, post=posts, ver_album=ver_album)



@main.route('/apropos_de_nous.html')
def apropos_de_nous():
 
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    lesvisteurs() #Visiteur compteur
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session

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
    lesvisteurs() #Visiteur compteur
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session
    
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

    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"

    return render_template('main/sondage.html',posts_pop=posts_pop, posts_pop_ver=posts_pop_ver, encours_rapport=encours_rapport,candidat=candidat,total_sondage=total_sondage, ver_encours=ver_encours,sondage_nom=sondage_nom, title=title, photos=photos, ver_album=ver_album)


@main.route('/sondage_rapport/<int:sond_id>.html')
def sondage_rapport(sond_id):
    title="Sondage"
    #Sondage encours
    encours=Encours.query.filter_by(id=sond_id).order_by(Encours.id.desc()).first_or_404()
    ver_encours="Vide"
    candidat=None
    lesvisteurs() #Visiteur compteur
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
     #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session

    if encours is not None:
        ver_encours="NoVide"
        candidat=Sondage.query.filter_by(encours_id=encours.id).order_by(Sondage.compteur.desc())
        candidat_totale=Sondage.query.filter_by(encours_id=encours.id).all()
        table_par_sondage=[] #Tableau valeur vendue
        for somme in candidat_totale:
            i=somme.id
            table_par_sondage.insert(0,i)
        total_sondage=len(table_par_sondage)
    sondage_nom=encours.titre

    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"

    return render_template('main/rapport_sondage.html',posts_pop=posts_pop, posts_pop_ver=posts_pop_ver, encours_rapport=encours_rapport,candidat=candidat,total_sondage=total_sondage, ver_encours=ver_encours,sondage_nom=sondage_nom, title=title, photos=photos, ver_album=ver_album)


@main.route('/galerie.html')
def galerie():

    title="Galerie"
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    lesvisteurs() #Visiteur compteur
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        photo=Photo.query.filter_by(album_id=album.id).all()#Photo
        ver_album='Novide'
     #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    #Les albums du Secteur de Lulenge
    album_autre=Album.query.all()
    ver_album_autre="Vide" #Vérification de l'album
    if album_autre is not None:
        ver_album_autre='NoVide'
    
    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"
    
    return render_template('main/galerie.html',posts_pop=posts_pop, posts_pop_ver=posts_pop_ver, photos_a=photo, ver_album_autre=ver_album_autre, album_autre=album_autre, encours_rapport=encours_rapport, title=title, photos=photos, ver_album=ver_album)



@main.route('/<int:galerie_id>/galerie.html')
def galerie_id(galerie_id):
    title="Galerie"
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session
    album_app=Album.query.filter_by(id=galerie_id).first_or_404() #Album
    lesvisteurs() #Visiteur compteur
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        photo=Photo.query.filter_by(album_id=album_app.id).all()#Photo
        ver_album='Novide'
     #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    #Les albums du Secteur de Lulenge
    album_autre=Album.query.all()
    ver_album_autre="Vide" #Vérification de l'album
    if album_autre is not None:
        ver_album_autre='NoVide'
    
    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"
    
    return render_template('main/galerie_une.html',posts_pop=posts_pop, posts_pop_ver=posts_pop_ver,  photos_a=photo, ver_album_autre=ver_album_autre, album_autre=album_autre, encours_rapport=encours_rapport, title=title, photos=photos, ver_album=ver_album)


@main.route('/actualite.html')
def actualite():
    lesvisteurs() #Visiteur compteur
    title="Actualité"
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    #Pagination de 50 candidature
    page= request.args.get('page', 1, type=int)  
    posts=Contenu.query.filter_by(status=True).order_by(Contenu.id.desc()).paginate(page=page, per_page=10)
    ver_controle_post="Vide"    
    if posts is not None:
        ver_controle_post="NoVide"
    #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    ver_rapport="Vide"
    if encours_rapport is not None:
        ver_rapport="NoVide"

    
    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"

    #Vérification de la rubrique
    rubrique_publication=Rubrique.query.filter_by(status=True).all()
    ver_rubrique="Vide"
    if rubrique_publication is not None:
        ver_rubrique="Novide"
    return render_template('main/actualite.html', ver_rapport=ver_rapport, ver_rubrique=ver_rubrique, posts_pop_ver=posts_pop_ver, rubrique_publication=rubrique_publication,ver_album=ver_album, posts=posts, posts_pop=posts_pop, ver_controle_post=ver_controle_post,  encours_rapport=encours_rapport, title=title, photos=photos)


@main.route('/<int:contenu_id>/<string:slug>')
def actualite_vue(contenu_id, slug):
    lesvisteurs() #Visiteur compteur
    title="Actualité"
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    #Article ouvert
    posts=Contenu.query.filter_by(slug=slug, id=contenu_id).first_or_404()
    #Nombre de lus de l'article
    if posts is not None:
        session["id_pu"] = posts.id

    article=ver_enre_article()
    var_lu_art=ver_enre_lu()

    if current_user.is_authenticated:
        pass
    else:
        if article is None and var_lu_art==False:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
        elif article==posts.id and var_lu_art==False:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
        elif article!=posts.id:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
    #Formulaire de commentaire
    form=CommentaireUnForm()
    #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    ver_rapport="Vide"
    if encours_rapport is not None:
        ver_rapport="NoVide"

    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"

    #Vérification de la rubrique
    rubrique_publication=Rubrique.query.filter_by(status=True).all()
    ver_rubrique="Vide"
    if rubrique_publication is not None:
        ver_rubrique="Novide"
    
    
    commentaire_visteur=Commentaire.query.filter_by(status=True, contenu_id=contenu_id).order_by(Commentaire.id.asc())
    commentaire_reponse=Comment.query.filter_by(status=True).order_by(Comment.id.asc())
    visteur_control="Vide"
    reponse="Vide"
    if commentaire_visteur is not None:
        visteur_control="Novide" 
    if commentaire_reponse is not None:
        reponse="Novide" 



    return render_template('main/un_vue.html',form=form,commentaire_visteur=commentaire_visteur, commentaire_reponse=commentaire_reponse, 
                            ver_rapport=ver_rapport, ver_rubrique=ver_rubrique, posts_pop_ver=posts_pop_ver, 
                            rubrique_publication=rubrique_publication,ver_album=ver_album, posts=posts, posts_pop=posts_pop,
                            encours_rapport=encours_rapport, title=title, photos=photos, visteur_control=visteur_control, reponse=reponse)

#Like de page
@main.route('/info-<int:contenu_id>/<string:slug>', methods=['GET','POST'])
def likepage(contenu_id, slug):
   #Vérification de la poste
   posts=Contenu.query.filter_by(slug=slug, id=contenu_id).first_or_404()
   #Verification de l'adresse mac de l'utilsiateur
   id_visteur_com=user_mac() #ID du visteur

   if current_user.is_authenticated:
        return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))

   if request.method=='GET':
      like_page=Like.query.filter_by(visiteur_id=id_visteur_com, contenu_id=contenu_id).first()
      if like_page is None:
         visteur_like=Like(visiteur_id=id_visteur_com, contenu_id=contenu_id)
         db.session.add(visteur_like)
         db.session.commit()
         #Incrimatentaion de la mention like
         if True:
            posts.like=posts.like+1
            db.session.commit()
            return redirect( url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug) )
      else:
         Like.query.filter_by(visiteur_id=id_visteur_com, contenu_id=contenu_id).delete()
         #Decrimatentaion de la mention like
         if True:
            posts.like=posts.like-1
            db.session.commit()
            return redirect( url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug) )
    #Nombre des lis de l'article
    
      #Commentaire des visteurs
   
   return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))


#Commentaire commentaire principale
@main.route('/comment_un-<int:contenu_id>/<string:slug>', methods=['GET','POST'])
def commenteurun(contenu_id, slug):
   #Commentaire
   if current_user.is_authenticated:
        return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))

   posts=Contenu.query.filter_by(slug=slug, id=contenu_id).first_or_404()
   form=CommentaireUnForm()
   id_visteur_com=user_mac() #ID du visteur
   #Enregistrement de commentaire
   if form.validate_on_submit():
      comm=Commentaire(contenu=form.commentaireun.data, status=True, visiteur_id=id_visteur_com, contenu_id=contenu_id)
      db.session.add(comm)
      db.session.commit()
      #Incrumentation de la commentaire
      if True:
         posts.comment=posts.comment+1
         db.session.commit()
      return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))
   return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))


@main.route('/<int:commentaire_id>_r_<int:contenu_id>/<string:slug>')
def actualite_vue_r(contenu_id, slug, commentaire_id):
    lesvisteurs() #Visiteur compteur
    title="Actualité"
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
    #Article ouvert
    posts=Contenu.query.filter_by(slug=slug, id=contenu_id).first_or_404()
    #Nombre de lus de l'article
    if posts is not None:
        session["id_pu"] = posts.id

    article=ver_enre_article()
    var_lu_art=ver_enre_lu()

    if current_user.is_authenticated:
        pass
    else:
        if article is None and var_lu_art==False:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
        elif article==posts.id and var_lu_art==False:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
        elif article!=posts.id:
                article_nombre_lu=posts.lus+1
                posts.lus=article_nombre_lu
                db.session.commit()
                session["ver"]=True
    #Formulaire de commentaire
    form=CommentaireUnForm()
    #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    ver_rapport="Vide"
    if encours_rapport is not None:
        ver_rapport="NoVide"

    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"

    #Vérification de la rubrique
    rubrique_publication=Rubrique.query.filter_by(status=True).all()
    ver_rubrique="Vide"
    if rubrique_publication is not None:
        ver_rubrique="Novide"
    
    
    commentaire_visteur=Commentaire.query.filter_by(status=True, contenu_id=contenu_id).order_by(Commentaire.id.asc())
    commentaire_reponse=Comment.query.filter_by(status=True).order_by(Comment.id.asc())
    visteur_control="Vide"
    reponse="Vide"
    if commentaire_visteur is not None:
        visteur_control="Novide" 
    if commentaire_reponse is not None:
        reponse="Novide" 



    return render_template('main/r_un_vue.html', commentaire_id=commentaire_id, form=form,commentaire_visteur=commentaire_visteur, commentaire_reponse=commentaire_reponse, 
                            ver_rapport=ver_rapport, ver_rubrique=ver_rubrique, posts_pop_ver=posts_pop_ver, 
                            rubrique_publication=rubrique_publication,ver_album=ver_album, posts=posts, posts_pop=posts_pop,
                            encours_rapport=encours_rapport, title=title, photos=photos, visteur_control=visteur_control, reponse=reponse)


#Commentaire commentaire principale
@main.route('/<int:commentaire_id>-comment_deux-<int:contenu_id>/<string:slug>', methods=['GET','POST'])
def commenteurdeux(commentaire_id, contenu_id, slug):

   if current_user.is_authenticated:
        return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))
  
   #Commentaire
   posts=Contenu.query.filter_by(slug=slug, id=contenu_id).first_or_404()
   form=CommentaireUnForm()
   id_visteur_com=user_mac() #ID du visteur
   #Enregistrement de commentaire
   if form.validate_on_submit():
      comm=Comment(contenu=form.commentaireun.data, status=True, visiteur_id=id_visteur_com, commentaire_id=commentaire_id)
      db.session.add(comm)
      db.session.commit()
      #Incrumentation de la commentaire
      if True:
         posts.comment=posts.comment+1
         db.session.commit()
      return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))
   return redirect(url_for('main.actualite_vue', contenu_id=contenu_id, slug=slug))


@main.route('/contact.html')
def contact():

    title="Contact"
    session.pop('ver', None) # Suppression de la session
    session.pop('id_pu', None) # Supression de la session
    #Album photo disponible
    album=Album.query.filter_by(statut=True).order_by(Album.id.desc()).first() #Album
    ver_album='Vide'
    lesvisteurs() #Visiteur compteur
    #Album photo
    if album is not None:
        photos=Photo.query.filter_by(album_id=album.id).limit(6) #Photo
        ver_album='Novide'
     #Rapport de encours
    encours_rapport=Encours.query.all()#Sondage en cours
    #Les albums du Secteur de Lulenge
    album_autre=Album.query.all()
    ver_album_autre="Vide" #Vérification de l'album
    if album_autre is not None:
        ver_album_autre='NoVide'
    
    #Vérification des articles populaire.
    posts_pop=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).limit(10)
    posts_pop_c=Contenu.query.filter(Contenu.lus >=5).order_by(Contenu.lus.desc()).first()
    posts_pop_ver="Vide"
    if posts_pop_c is not None:
        posts_pop_ver="NoVide"
    
    
    
    return render_template('main/contact.html',posts_pop=posts_pop, posts_pop_ver=posts_pop_ver,  ver_album_autre=ver_album_autre, album_autre=album_autre, encours_rapport=encours_rapport, title=title, photos=photos, ver_album=ver_album)


