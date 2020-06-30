from flask import request, jsonify

from webapp.app.api import bp
from webapp import endpoint_config


@bp.route('/players', methods=['GET'])
def get_players():
    return endpoint_config.ENDPOINTS[request.path]()


@bp.route('/upload_tweets', methods=['POST'])
def upload_tweets():
    return endpoint_config.ENDPOINTS[request.path](request.json)

@bp.route('/followed_accounts', methods=['GET'])
@bp.route('/followed_accounts/id/<user_id>', methods=['GET'])
@bp.route('/followed_accounts/handle/<user_name>', methods=['GET'])
def check_tweets(user_id=None, user_name=None):
    return endpoint_config.ENDPOINTS['/api/followed_accounts'](user_id, user_name)
