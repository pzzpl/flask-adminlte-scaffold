from flask import Blueprint

class_pkg = Blueprint('class', __name__)

from . import views

