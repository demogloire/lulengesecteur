import random
import string
import uuid
import os
import secrets
from PIL import Image
from .. import create_app
from .. import db
from ..models import Visiteur

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/posts/page', picture_fn)
    output_sz = (1500 ,1000)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)

    return picture_fn

def save_picture_thumb(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/posts/thumb', picture_fn)
    output_sz = (500 ,375)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)

    return picture_fn

def code_usermac(length=6):
    #Code pour généer un mot de passe unique
    your_letters='AEIOU1234567890'
    return ''.join((random.choice(your_letters) for i in range(length)))


#Adresse mac unique
def macadress():
    var=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return var

#Ideintification de l'utilisateur sur base de l'adresse MAC
def user_mac():
    adre_unique_mac=macadress()
    code_user=code_usermac()
    verification_visteur=Visiteur.query.filter_by(adress_mac=adre_unique_mac).first()
    if verification_visteur is None:
        visiteur_user=Visiteur(pseudo=code_user, adress_mac=adre_unique_mac)
        db.session.add(visiteur_user)
        db.session.commit()
        return visiteur_user.id
    else:
        return verification_visteur.id