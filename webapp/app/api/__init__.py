from flask import Blueprint

bp = Blueprint('api', __name__)

from webapp.app.api import routes