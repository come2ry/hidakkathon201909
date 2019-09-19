from flask import Flask
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    app.secret_key = os.getenv("API_SECRET_KEY", None)

    return app


app = create_app()