from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Contenu, File, Statistique
from app.posts.forms import AjouterArticleForm, EditerArticleForm
from app.posts.others_posts import save_picture, save_picture_thumb
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify, Slugify, UniqueSlugify

from . import posts

@posts.route('/ajouter_article', methods=['GET', 'POST'])
@login_required
def ajouter_article():
    
    #Formulaire d'ajout des informations de l'article
    form=AjouterArticleForm()
    #Envoi du formulaire des informations
    if form.validate_on_submit():
        if form.picture.data:
            #Enregistrement des infromation de la poste
            titre_cap=form.titre.data
            titre_slugify = Slugify(to_lower=True)
            imagefile_thumb= save_picture_thumb(form.picture.data)
            post=Contenu(titre=titre_cap.capitalize(), cont=form.cont.data, thumb=imagefile_thumb, descrip_image=form.descrip_image.data,slug=titre_slugify(form.titre.data), rub_cont=form.rubrique.data, cont_user=current_user)
            db.session.add(post)
            db.session.commit()
            #Enregistrement de l'image dans la base des données
            imagefile= save_picture(form.picture.data)
            file_user=File(nom_file=imagefile, cont_file=post)
            db.session.add(file_user)
            db.session.commit()
            #Enregistrement de l'information de statistqiue
            stat=Statistique(contenu_nombre=0, cont_stat=post)
            db.session.add(stat)
            db.session.commit()
        else:
            flash("Chaque article doit avoir une image",'danger')
            return redirect(url_for('posts.ajouter_article'))
        flash('ajouter reussie','success')
        return redirect(url_for('posts.tous_articles'))
    return render_template('posts/ajouterpost.html', title="Welcome", form=form)

@posts.route('/tous_articles')
@login_required
def tous_articles():
    page= request.args.get('page', 1, type=int)
    post_page=Contenu.query.order_by(Contenu.date_post.desc()).paginate(page=page, per_page=5)

    return render_template('posts/allposts.html', title="Welcome", posts=post_page)

@posts.route('/tous_articles/<int:post_id>', methods=['GET', 'POST'])
@login_required
def statuts_id(post_id):

    contenus=Contenu.query.filter_by(id=post_id).first_or_404()
    if contenus is None:
        return redirect(url_for('posts.tous_articles'))
    else:
        if contenus.cont_user.id != current_user.id:
            flash(" Vous ne pas l'auteur", 'danger')
            return redirect(url_for('posts.tous_articles'))
        else:
            if contenus.status == 1:
                contenus.status = 0
                db.session.commit()
                flash("L'article vient d'etre désactivé sur la plateforme",'success')
                return redirect(url_for('posts.tous_articles'))
            elif contenus.status == 0:
                contenus.status = 1
                db.session.commit()
                flash("L'article vient d'etre activé sur la plateforme",'success')
                return redirect(url_for('posts.tous_articles'))
    return render_template('posts/allposts.html')


@posts.route('/apercu/<int:post_id>')
@login_required
def apercu(post_id):
    post=Contenu.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('posts.tous_articles'))
    else:
        image=File.query.filter_by(cont_file=post).first_or_404()
        image_file= url_for('static', filename='posts/page/'+image.nom_file)
            
    return render_template('posts/apercu.html', post=post, image_file=image_file)



@posts.route('/editer_posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editer_posts(post_id):

    form=EditerArticleForm()

    post=Contenu.query.filter_by(id=post_id).first_or_404()
    file=File.query.filter_by(cont_file=post).first_or_404()
    if post is None:
        return redirect(url_for('posts.tous_articles'))
    else:
        if form.validate_on_submit():
            titre_slugify = Slugify(to_lower=True)
            if form.pictureed.data:
                image=save_picture(form.pictureed.data)
                thumb=save_picture_thumb(form.pictureed.data)
                post.thumb=thumb
                file.nom_file=image
            post.titre=form.titreed.data.capitalize()
            post.slug=titre_slugify(form.titreed.data)
            post.cont=form.conted.data
            post.descrip_image=form.descrip_imageed.data
            post.cont_file=form.rubriqueed.data
            db.session.commit()
            flash("L'article vient d'etre modifié",'success')
            return redirect(url_for('posts.apercu', post_id=post.id ))
        elif request.method =='GET':
            form.titreed.data=post.titre
            form.conted.data=post.cont
            form.descrip_imageed.data=post.descrip_image
            form.rubriqueed.data=post.rub_cont.nom
            
    return render_template('posts/editer_posts.html', form=form)



