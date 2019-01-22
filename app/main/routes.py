from flask import render_template

from . import main

@main.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('homepage.html', title="Welcome")