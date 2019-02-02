from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Rubrique


class RubriqueForm(FlaskForm):
    nom_rub= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=20)])
    submit_rub = SubmitField('Enregister')

    #Foction de la verification d'unique existenace dans la base des données
    def validate_nom_rub(self, nom_rub):
        rubrique= Rubrique.query.filter_by(nom=nom_rub.data).first()
        if rubrique:
            raise ValidationError("Cette rubrique existe déjà")

class EditerRubriqueForm(FlaskForm):
    nomedrub= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=20)])
    submitedrub = SubmitField('Mise à jour')

    #Foction de la verification d'unique existenace dans la base des données
    def validate_nomedrub(self, nomedrub):
        rubrique= Rubrique.query.filter_by(nom=nomedrub.data).first()
        if rubrique:
            raise ValidationError("Cette rubrique existe déjà")
    
