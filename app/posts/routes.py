from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Contenu
from app.posts.forms import AjouterArticleForm
#from app.users.others_user import save_picture
from flask_login import login_user, current_user, logout_user, login_required

from . import posts

@posts.route('/ajouter_article', methods=['GET', 'POST'])
@login_required
def ajouter_article():
 
    form=AjouterArticleForm()

    if form.validate_on_submit():
        flash(form.rubrique.data,'success')
    
    return render_template('posts/ajouterpost.html', title="Welcome", form=form)