from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

login_manager.session_protection = "strong"

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    try:
      assert config_name == "development" or config_name == "production"
      app.config.from_object(app_config[config_name])
    except AssertionError:
      print ("[!] Helix production config not set... running in development state.")
      app.config.from_object(app_config['development'])
    from os import environ
    app.config.from_pyfile('config.py')
    Bootstrap(app)

    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
      return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
      return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
      return render_template('errors/500.html', title='Server Error'), 500

    return app, db

