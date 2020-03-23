import os
import secrets
from PIL import Image
from .. import create_app

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