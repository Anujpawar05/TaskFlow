from flask import Flask

from .models import db


def create_app():
    app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app