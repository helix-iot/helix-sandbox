from flask import Blueprint

__author__ = "m4n3dw0lf"

auth = Blueprint('auth', __name__)

from . import views
