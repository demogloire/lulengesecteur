from flask import render_template, flash, url_for, redirect, request

from . import authentification 
from .. import db, bcrypt
from ..models import User
from app.authentification.forms import LoginForm
from flask_login import login_user, current_user


@authentification.route('/login',  methods=['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
       ## Vérification de l'existence d'au moins un administrateur
    ver_admini_existe= User.query.filter_by(status=True).first()
    if ver_admini_existe is None:
      return redirect(url_for('users.register_ed'))

    
    form=LoginForm() 

    if form.validate_on_submit():
           
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.dashboard'))
        else:
            flash("E-mail ou mot de passe incorrect",'danger')

    return render_template('authentification/login.html', title="Login", form=form)


