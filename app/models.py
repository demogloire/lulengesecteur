
from app import db
from datetime import datetime


class Rubrique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    contenus = db.relationship('Contenu', backref='rub_cont', lazy='dynamic')
    

    def __repr__(self):
        return f"Rubrique('{self.nom}')"


class Contenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    cont=db.Column(db.Text)
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    status = db.Column(db.Boolean, default=False)
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
    def __repr__(self):
        return f"File('{self.nom_file}')"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    post_nom = db.Column(db.String(128), nullable=False)
    prenom = db.Column(db.String(128), nullable=False)
    fonction = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
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


