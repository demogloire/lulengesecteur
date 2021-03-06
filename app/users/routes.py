from flask import render_template, flash, url_for, redirect, request
from . import users 
from .. import db, bcrypt
from ..models import User, Album, Contenu, Internaute, Encours, Visiteur
from app.users.forms import EditerUserForm, RegisterForm, EditerPasswordForm
from app.users.others_user import save_picture
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date


#Enregistrement des utilisateurs sur la plateforme
@users.route('/register',  methods=['GET','POST'])
@login_required
def register():

    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        utilisateur= User(nom=form.nom.data, post_nom=form.post_nom.data, prenom=form.prenom.data, username=form.username.data,password=hashed_password)
        db.session.add(utilisateur)
        db.session.commit()
        flash('Creation de compte avec succes','success')
        #return redirect(url_for('authenfication.'))
        return redirect(url_for('users.all_user'))

    return render_template('user/register.html', title="Enregistrement", form=form)


#Liste des administrateurs du site web 
@users.route('/all_user')
@login_required
def all_user():
    #Requete de tous les utilisateurs
    users= User.query.all()
    
    return render_template('user/alluser.html', title="Les utilisateurs", users=users)


#Activation du statut des utilisateurs
@users.route('/statuts_id/<int:user_id>',methods=['GET','POST'])
@login_required
def statuts_id(user_id):
    
    user=User.query.filter_by(id=user_id).first_or_404()
    if user is None:
        return redirect(url_for('users.dashboard'))
    else:
        if user.id==current_user.id:
            flash('Vous êtes connecté, impossible de changez votre statut', 'danger')
            return redirect(url_for('users.all_user'))
        else:
            if user.status == 1:
                user.status = 0
                db.session.commit()
                flash("L'utilisateur est désactivé sur la plateforme",'success')
                return redirect(url_for('users.all_user'))
            elif user.status == 0:
                user.status = 1
                db.session.commit()
                flash("L'utilisateur est activé sur la plateforme",'success')
                return redirect(url_for('users.all_user'))
    return render_template('user/alluser.html')


#Profil et mise à jour de l'utilisateurs
@users.route('/profil/<int:user_id>',  methods=['GET','POST'])
@login_required
def profil(user_id):

    title="Compte de {} ".format(current_user.prenom) 
    #Requete d'affichage d'un utilisateur par son ID avec resique de 404
    profil= User.query.filter_by(id=user_id).first_or_404()
    #Lien dynamique
    image_file= url_for('static', filename='profil/{}'.format(profil.image_file))
    #Avatar par defaut
    if profil.image_file == 'default.png':
        mesure = '300px'#Mesure de l'avatar
    else:
        mesure = False
    #Procedure de mise à jour et injection des données dans le formulaire

    #Formulaire
    form=EditerUserForm()

    if request.method =='GET':
        form.nom_ed.data=profil.nom
        form.post_nom_ed.data=profil.post_nom
        form.prenom_ed.data=profil.prenom
        form.username_ed.data=profil.username

    return render_template('user/profil.html', form=form, profil=profil, image_file=image_file, mesure=mesure,  image=profil.image_file, title=title )

#Mise à jour des information de l'utilisateur
@users.route('/editer_user',methods=['GET','POST'])
@login_required
def editer_user():

    #Titre du site web
    title="Modifier utilisateur"
    #Formulaire d'etidtion de l'utilisateur
    form=EditerUserForm()
    #procedure d'injection et des mise a jour
    if form.validate_on_submit():
    #if request.method=='POST': 
        if form.picture_ed.data:
            imagefile= save_picture(form.picture_ed.data)
            current_user.image_file=imagefile
        current_user.nom=form.nom_ed.data
        current_user.post_nom=form.post_nom_ed.data
        current_user.prenom=form.prenom_ed.data
        current_user.username=form.username_ed.data
        db.session.commit()
        return redirect(url_for('users.profil', user_id=current_user.id ))
    elif request.method == 'GET':
        form.nom_ed.data=current_user.nom
        form.post_nom_ed.data=current_user.post_nom
        form.prenom_ed.data=current_user.prenom
        form.username_ed.data=current_user.username
    return render_template('user/editeruser.html', form=form, title=title  )

#Tableau de bord
@users.route('/dashboard')
@login_required
def dashboard():
    #Nombre variable
    contenu_pub=Contenu.query.all()
    like_nombre_contenu=[] #Tableau de like
    cmt_nombre_contenu=[] #Tableau de commentaire
    vue_nombre_contenu=[] #Tableau de vue
    for somme in contenu_pub:
        i=somme.lus
        b=somme.like
        c=somme.comment
        like_nombre_contenu.insert(0,b)
        cmt_nombre_contenu.insert(0,c)
        vue_nombre_contenu.insert(0,i)
    total_like=sum(like_nombre_contenu)
    total_cmt=sum(cmt_nombre_contenu)
    total_vue=sum(vue_nombre_contenu)

    #Visiteur par date
    date_aujour=date.today()
    les_visiteurs=Internaute.query.filter_by(date_vist=date_aujour).first()
    visiteur=0
    if les_visiteurs is not None:
        visiteur=les_visiteurs.nombre_vis
    #Transformation de la date
    mois_encours=date.today()
    date_format_avant=str(mois_encours).split("-")
    date_graphique="{}-{}".format(date_format_avant[0],date_format_avant[1]) #La date formatée mensuellement
    mois='%{}%'.format(date_graphique) 
    #Triage des visites selons le mois
    les_viisteur_mensuel=Internaute.query.filter(Internaute.date_vist.ilike(mois)).all()
    label=[] #Tableau de label
    series=[] #Tableau de serie
    for somme in les_viisteur_mensuel:
        i=somme.date_vist
        b=somme.nombre_vis
        label.insert(0,i)
        series.insert(0,b)
    
    print(label,'label',series,'series')
    
    return render_template('authentification/dashboard.html',label=label, series=series, visiteur=visiteur, total_like=total_like, total_cmt=total_cmt, total_vue=total_vue, title="Dashboard")







#Modification de l'utilisateur
@users.route('/editerpass', methods=['GET','POST'])
@login_required
def editerpass():

    form=EditerPasswordForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password=hashed_password
        db.session.commit()
        flash('Votre mot de passe est modifier avec succès','success')
        return redirect(url_for('users.profil', user_id=current_user.id ))
    return render_template('user/editerpass.html', form=form, title="Modifier mot de passe")

#Déconnexion sur la plateforme
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('authentification.login'))


#Page des configuration
@users.route('/configuration')
@login_required
def configuration():
    title='Configuration'
    return render_template('user/configuration.html', title=title)



#Enregistrement des utilisateurs sur la plateforme
@users.route('/register_ed',  methods=['GET','POST'])
def register_ed():

    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        utilisateur= User(nom=form.nom.data, status=True, post_nom=form.post_nom.data, prenom=form.prenom.data, username=form.username.data,password=hashed_password)
        db.session.add(utilisateur)
        db.session.commit()
        flash('Un compte admin crée avec succès','success')
        #return redirect(url_for('authenfication.'))
        return redirect(url_for('authentification.login'))

    return render_template('user/registered.html', title="Administrateur", form=form)



