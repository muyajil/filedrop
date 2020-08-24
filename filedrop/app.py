import os

from flask import Flask

from .blueprints.upload import upload_bp
from .blueprints.download import download_bp
from .blueprints.index import index_bp
from .cron import crontab


def create_app():
    template_dir = os.path.abspath('./filedrop/templates')
    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(download_bp, url_prefix="/download")
    app.register_blueprint(index_bp)
    crontab.init_app(app)
    app.secret_key = b'secret'
    return app
