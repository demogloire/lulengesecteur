
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user

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
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    status = db.Column(db.Boolean, default=False)
    descrip_image = db.Column(db.String(255))
    thumb = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    files = db.relationship('File', backref='cont_file', lazy='dynamic')
    statistiques = db.relationship('Statistique', backref='cont_stat', lazy='dynamic')
    rubrique_id = db.Column(db.Integer, db.ForeignKey('rubrique.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Contenu('{self.titre}','{self.cont}')"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_file = db.Column(db.String(128))
    contenu_id = db.Column(db.Integer, db.ForeignKey('contenu.id'), nullable=False)
    thumb=db.Column(db.String(128))
    def __repr__(self):
        return f"File('{self.nom_file}')"

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

class Statistique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor= db.Column(db.Integer)
    contenu_nombre= db.Column(db.Integer)
    contenu_id = db.Column(db.Integer, db.ForeignKey('contenu.id'), nullable=False)

    def __repr__(self):
        return f"Statistique('{self.visitor}','{self.contenu_nombre}')"


