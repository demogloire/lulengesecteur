from flask import Blueprint

authentification = Blueprint('authentification','__name__',url_prefix='/auth')

from . import routes