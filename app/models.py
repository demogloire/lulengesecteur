
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Rubrique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    status = db.Column(db.Boolean, default=False)
    contenus = db.relationship('Contenu', backref='rub_cont', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.nom)

class Contenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    cont=db.Column(db.Text)
    date_p = db.Column(db.Date, nullable=False, default=datetime.utcnow )
    status = db.Column(db.Boolean, default=False)
    descrip_image = db.Column(db.String(255))
    thumb = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    like=db.Column(db.Integer, default=0)
    comment=db.Column(db.Integer, default=0)
    rubrique_id = db.Column(db.Integer, db.ForeignKey('rubrique.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commentaires = db.relationship('Commentaire', backref='com_cont', lazy='dynamic')
    
    def __repr__(self):
        return f"Contenu('{self.titre}','{self.cont}')"

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu=db.Column(db.Text)
    date_com = db.Column(db.Date, nullable=False, default=datetime.utcnow )
    status = db.Column(db.Boolean, default=False)
    contenu_id = db.Column(db.Integer, db.ForeignKey('contenu.id'), nullable=False)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)
    comments = db.relationship('Comment', backref='commentaire_cont', lazy='dynamic')

    
    def __repr__(self):
        return f"Commentaire('{self.contenu}','{self.date_com}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu=db.Column(db.Text)
    date_com = db.Column(db.Date, nullable=False, default=datetime.utcnow )
    status = db.Column(db.Boolean, default=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaire.id'), nullable=False)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)
    
    def __repr__(self):
        return f"Comment('{self.contenu}','{self.date_com}')"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    post_nom = db.Column(db.String(128), nullable=False)
    prenom = db.Column(db.String(128), nullable=False)
    #fonction = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
    username=db.Column(db.String(128), nullable=False)
    password=db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    contenus = db.relationship('Contenu', backref='cont_user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.nom}','{self.post_nom}','{self.status}')"

class Visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(128), nullable=False)
    adress_mac = db.Column(db.String(128), nullable=False)
    avatar= db.Column(db.String(128))
    comments = db.relationship('Comment', backref='visiteur_comment', lazy='dynamic')
    commentaires = db.relationship('Commentaire', backref='visiteur_commentaire', lazy='dynamic')
    choice = db.relationship('Choice', backref='visiteur_choice', lazy='dynamic')


    def __repr__(self):
        return f"Visiteur('{self.pseudo}','{self.adress_mac}')"


class Encours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    status = db.Column(db.Boolean, default=False)
    sondages = db.relationship('Sondage', backref='encours_sondage', lazy='dynamic')

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_s= db.Column(db.Date, nullable=False, default=datetime.utcnow )
    sondage_id = db.Column(db.Integer, db.ForeignKey('sondage.id'), nullable=False)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)

  

class Sondage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noms = db.Column(db.String(128), nullable=False)
    partie = db.Column(db.String(128), nullable=False)
    avatar= db.Column(db.String(128))
    choices = db.relationship('Choice', backref='sondage_choix', lazy='dynamic')
    compteur= db.Column(db.Integer, default=0)
    encours_id = db.Column(db.Integer, db.ForeignKey('encours.id'), nullable=False)

    def __repr__(self):
        return f"Sondage('{self.noms}')"



class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noms = db.Column(db.String(128), nullable=False)
    photos = db.relationship('Photo', backref='photos_album', lazy='dynamic')
    statut= db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Album('{self.noms}')"

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    photo= db.Column(db.String(128))
    
    def __repr__(self):
        return f"Photo('{self.album_id}')"



