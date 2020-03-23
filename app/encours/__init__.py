from flask import Blueprint

encours = Blueprint('encours','__name__',url_prefix='/admin')

from . import routes