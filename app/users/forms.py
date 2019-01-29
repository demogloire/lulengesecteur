from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from flask_login import current_user
from .. import bcrypt

from ..models import User

class RegisterForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=20)])
    post_nom= StringField('Post-nom', validators=[DataRequired("Completer post-nom"),  Length(min=4, max=20)])
    prenom= StringField('Prénom', validators=[DataRequired("Completer prénom"),  Length(min=3, max=20)])
    username= StringField('E-mail', validators=[DataRequired("Completer mail"), Email("E-mail invalide")])
    password= PasswordField('Mot de passe', validators=[DataRequired("Completer Mot de passe"), Length(min=6, max=225)])
    confirm_password= PasswordField('Confirmer mot de passe', validators=[DataRequired('Confirmer votre mot de passe'), EqualTo('password','Mot de passe non conforme')])
    picture = FileField('Mise à jour photo profil', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    submit = SubmitField('Enregister')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("E-mail existe")

class EditerUserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=20)])
    post_nom= StringField('Post-nom', validators=[DataRequired("Completer post-nom"),  Length(min=4, max=20)])
    prenom= StringField('Prénom', validators=[DataRequired("Completer prénom"),  Length(min=3, max=20)])
    username= StringField('E-mail', validators=[DataRequired("Completer mail"), Email("E-mail invalide")])
    password= PasswordField('Mot de passe', validators=[DataRequired("Completer Mot de passe"), Length(min=6, max=225)])
    confirm_password= PasswordField('Confirmer mot de passe', validators=[DataRequired('Confirmer votre mot de passe'), EqualTo('password','Mot de passe non conforme')])
    picture = FileField('Mise à jour photo profil', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    submit = SubmitField('Mise à jour')

    def validate_username(self, username):
        if username.data != current_user.username:
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("E-mail existe")

class EditerPasswordForm(FlaskForm):
    password= PasswordField('Mot de passe', validators=[DataRequired("Completer Mot de passe"), Length(min=6, max=225)])
    confirm_password= PasswordField('Confirmer mot de passe', validators=[DataRequired('Confirmer votre mot de passe'), EqualTo('password','Mot de passe non conforme')])
    submit = SubmitField('Mise à jour')

    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user.password, password.data):
            raise ValidationError("Vous avez répété l'ancien mot de passe")

