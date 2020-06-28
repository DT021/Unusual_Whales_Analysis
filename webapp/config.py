import os
from dotenv import load_dotenv
from webapp import webapp_parent

load_dotenv(os.path.join(webapp_parent, '.env'))


class WebAppConfig:
    PSYCOPG2_URL = os.environ.get('PSYCOPG2_URL')
