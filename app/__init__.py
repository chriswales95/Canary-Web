"""
This file initialises the application and follows the Application Factory pattern mentioned in the Flask documentation
here: https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
"""

from flask import Flask
from app.canary_interface import canary_interface
from app.frontend import frontend


def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Register blueprints
        app.register_blueprint(canary_interface, url_prefix='/canary/api/v1')
        app.register_blueprint(frontend, url_prefix='/')

        # Check if we have the canary models available
        from canary.argument_pipeline import get_models_not_on_disk

        if len(get_models_not_on_disk()) > 0:
            from canary.argument_pipeline import download_model
            download_model("all")

        return app
