from webapp.endpoints import *

ENDPOINTS = {
    '/api/players': get_players_from_db,
    '/api/upload_tweets': upload_tweets_to_db,
    '/api/followed_accounts': get_followed_accounts_from_db,
}