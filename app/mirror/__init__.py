from flask import Blueprint

mirror = Blueprint("mirror",__name__)

from . import views,forms