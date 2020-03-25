from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from wtf_tinymce import wtf_tinymce
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown


#from mysql import connector

#Importation des configuration de l'application sur le developpement de l'application
from config import app_config



db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

#Structure de l'application

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    #Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    wtf_tinymce.init_app(app)
    

    login_manager.login_message = "Veuillez vous connecté"
    login_manager.login_view = "authentification.login"
    login_manager.login_message_category ='danger'
    SimpleMDE(app)
    Markdown(app)
    migrate = Migrate(app, db)
    #md= Markdown(app, extensions=['fenced_code'])
    from app import models

    ''' 
    Utilisation des stucture Blueprint
    '''
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page non trouvée'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Erreur serveur'), 500

    #Autres pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Authetification de l'utilisateur sur la plateforme
    from .authentification import authentification as authentification_blueprint
    app.register_blueprint(authentification_blueprint)

    #Les pages du dashbord de l'l'adminnistrateur
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    #Les pages du dashbord, les posts
    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    #Les pages du dashbord, les posts
    from .rubriques import rubriques as rubriques_blueprint
    app.register_blueprint(rubriques_blueprint)

    #Ajout de l'album photo
    from .album import album as album_blueprint
    app.register_blueprint(album_blueprint)

    #Ajout Le sondage
    from .encours import encours as encours_blueprint
    app.register_blueprint(encours_blueprint)

    #Ajout Le sondage
    from .sondage import sondage as sondage_blueprint
    app.register_blueprint(sondage_blueprint)

    


    return app

