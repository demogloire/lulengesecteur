from flask import Blueprint

rubriques = Blueprint('rubriques','__name__',url_prefix='/admin')

from . import routes