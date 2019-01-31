from flask import render_template

from . import posts

@posts.route('/ajouter_article')
def ajouter_article():
 
    pass
    
    return render_template('homepage.html', title="Welcome")