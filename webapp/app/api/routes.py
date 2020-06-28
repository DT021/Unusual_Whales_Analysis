from flask import request

from webapp.app.api import bp
from webapp import endpoint_config


@bp.route('/players', methods=['GET'])
def get_players():
    return endpoint_config.ENDPOINTS[request.path]()