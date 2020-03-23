from flask import Blueprint

sondage = Blueprint('sondage','__name__',url_prefix='/admin')

from . import routes