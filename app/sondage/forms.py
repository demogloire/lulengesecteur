from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Encours


#Fonction d'énumeration des ribriques sur la plateforme
def encours_list():
    return Encours.query.filter_by(status=True)


class AjouterSondageForm(FlaskForm):
    noms= StringField('Titre', validators=[DataRequired("Completer le titre")])
    partie= StringField('Titre', validators=[DataRequired("Completer le titre")])
    picture = FileField('Mise à jour photo profil', validators=[DataRequired("Charger l'image svp"), FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    encours = QuerySelectField(query_factory=encours_list, get_label='titre', allow_blank=False)
    submit = SubmitField('Enregister')



class EditerSondageForm(FlaskForm):
    noms= StringField('Titre', validators=[DataRequired("Completer le titre")])
    partie= StringField('Titre', validators=[DataRequired("Completer le titre")])
    picture = FileField('Mise à jour photo profil', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    encours = QuerySelectField(query_factory=encours_list, get_label='titre', allow_blank=False)
    submit = SubmitField('Modifier')


# class EditerArticleForm(FlaskForm):
#     titreed= StringField('Titre', validators=[DataRequired("Completer le titre")])
#     conted= TextAreaField('Contenue', validators=[DataRequired("Completer le contenue")])
#     descrip_imageed= StringField('Prénom', validators=[DataRequired("Completer la description de l'image")])
#     pictureed = FileField('Mise à jour photo profil', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
#     rubriqueed = QuerySelectField(query_factory=rubrique_list, get_label='nom', allow_blank=False)
#     submited = SubmitField('Enregister')

#     #Fornction de verification d'unique existenace dans la base des données
#     def validate_titre(self, titreed):
#         cont= Contenu.query.filter_by(titre=titreed.data).first()
#         if cont:
#             raise ValidationError("Cet article existe déjà")



