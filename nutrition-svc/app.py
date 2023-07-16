from flask import Flask
from flask_restful import Api

from Resources import resources
from Common import Config


def create_app():
    """
    """
    app = Flask(__name__)

    api = Api(app)
    resources.load_resources(api)

    return app


if __name__ == "__main__":
    nutrition_app = create_app()
    nutrition_app.run(debug=Config.AppConfig.DEBUG,
                      port=Config.AppConfig.PORT)
