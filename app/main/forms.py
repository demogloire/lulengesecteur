from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField



class CommentaireUnForm(FlaskForm):
    commentaireun= TextAreaField('Commentaire', validators=[DataRequired("Votre commentaire")])
    submit = SubmitField('Commenter')
