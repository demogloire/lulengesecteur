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
    picture_path = os.path.join(app.root_path, 'static/profil', picture_fn)
    output_sz = (300,301)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)

    return picture_fn
