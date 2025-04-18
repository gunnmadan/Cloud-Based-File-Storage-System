from flask import Blueprint

# Create the blueprint
files = Blueprint('files', __name__)

# Import routes so they are registered when the app starts
from .routes import *  

