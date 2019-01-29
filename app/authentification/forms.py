from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username= StringField('E-mail', validators=[DataRequired("Completer l'email"), Email('Adresse invalide')])
    password= PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Souvenez-vous')
    submit = SubmitField('Connexion')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user.status==0:
            raise ValidationError("Vous êtes bloqué sur la plateforme")
        
