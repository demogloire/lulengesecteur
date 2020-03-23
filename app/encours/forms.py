from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Encours


class EncoursForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=126)])
    submit= SubmitField('Enregister')

    #Foction de la verification d'unique existenace dans la base des données
    def validate_nom(self, nom):
        encours= Encours.query.filter_by(titre=nom.data).first()
        if encours:
            raise ValidationError("Cette rubrique existe déjà")


    
