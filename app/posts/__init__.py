from flask import Blueprint

posts = Blueprint('posts','__name__',url_prefix='/admin')

from . import routes