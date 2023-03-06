from flask import Flask, render_template
from werkzeug.exceptions import ServiceUnavailable

from db.models import User

from proxies import user


def app_register_blueprints(app: Flask) -> None:
    from blueprints.auth import bp as auth_bp
    from blueprints.account import bp as account_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)


def app_register_commands(app: Flask) -> None:
    from commands import create_admin, delete_admin, list_admins

    app.cli.add_command(create_admin)
    app.cli.add_command(delete_admin)
    app.cli.add_command(list_admins)


def app_set_default_handlers(app: Flask) -> None:
    @app.get("/")
    def root():
        return render_template("index.j2")

    @app.errorhandler(ServiceUnavailable)
    def service_unavailable(http_error):
        return render_template("503.j2")


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.jinja_env.globals.update(user=user)
    
    app_register_commands(app)
    app_register_blueprints(app)
    app_set_default_handlers(app)

    return app

