from flask import Blueprint

major = Blueprint('major', __name__)

from . import views
