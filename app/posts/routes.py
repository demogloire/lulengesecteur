from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Contenu
from app.posts.forms import AjouterArticleForm, EditerArticleForm
from app.posts.others_posts import save_picture, save_picture_thumb
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify, Slugify, UniqueSlugify

from . import posts

@posts.route('/ajouter_article', methods=['GET', 'POST'])
@login_required
def ajouter_article():
    
    title="Ajouter article"
    #Formulaire d'ajout des informations de l'article
    form=AjouterArticleForm()
    #Envoi du formulaire des informations
    if form.validate_on_submit():
        if form.picture.data:
            #Enregistrement des infromation de la poste
            titre_cap=form.titre.data
            titre_slugify = Slugify(to_lower=True)
            imagefile_thumb= save_picture_thumb(form.picture.data)
            post=Contenu(titre=titre_cap.capitalize(), cont=form.cont.data, thumb=imagefile_thumb,slug=titre_slugify(form.titre.data), rub_cont=form.rubrique.data, cont_user=current_user)
            db.session.add(post)
            db.session.commit()
            flash('ajouter reussie','success')
            return redirect(url_for('posts.tous_articles'))        
    return render_template('posts/ajouterpost.html', title=title, form=form)

@posts.route('/tous_articles')
@login_required
def tous_articles():
    title='Liste des articles'
    page= request.args.get('page', 1, type=int)
    post_page=Contenu.query.order_by(Contenu.date_p.desc()).paginate(page=page, per_page=5)

    return render_template('posts/allposts.html', title=title, posts=post_page)

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
    title= '{}'.format(post.titre) 
            
    return render_template('posts/apercu.html', post=post, title=title)



@posts.route('/editer_posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editer_posts(post_id):

    form=EditerArticleForm()

    post=Contenu.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('posts.tous_articles'))
    else:
        if form.validate_on_submit():
            if form.pictureed.data:
                thumb=save_picture_thumb(form.pictureed.data)
                post.thumb=thumb
            post.titre=form.titreed.data.capitalize()
            post.cont=form.conted.data
            post.cont_file=form.rubriqueed.data
            db.session.commit()
            flash("L'article vient d'etre modifié",'success')
            return redirect(url_for('main.actualite_vue', contenu_id=post.id, slug=post.slug))
        elif request.method =='GET':
            form.titreed.data=post.titre
            form.conted.data=post.cont
            form.rubriqueed.data=post.rub_cont
            
    return render_template('posts/editer_posts.html', form=form)



