from flask import render_template
from ..models import Contenu, File
from . import main

@main.route('/')
def homepage():

    posts=Contenu.query.filter_by(status=True).order_by(Contenu.date_post.desc()).limit(2)
    
    return render_template('main/homepage.html', title="Bienvenu Secteur lulenge fizi", posts=posts)