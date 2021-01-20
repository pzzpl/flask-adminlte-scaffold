from flask import Blueprint

alloc = Blueprint('alloc', __name__)

from . import views
