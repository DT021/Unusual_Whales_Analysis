from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from webapp.config import WebAppConfig

# initialize extensions outside of app context
# sqa = SQLAlchemy()


def create_app(config_class=WebAppConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    from webapp.app import db
    # bind extensions to app
    # sqa.init_app(app)
    db.init_app(app)

    from webapp.app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
