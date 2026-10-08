import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["240 per day", "60 per hour"])

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///codeforge.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        ADSENSE_CLIENT_ID=os.getenv("ADSENSE_CLIENT_ID", ""),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("SECURE_COOKIES", "0") == "1",
    )
    if test_config: app.config.update(test_config)
    db.init_app(app); migrate.init_app(app, db); csrf.init_app(app); limiter.init_app(app)
    login_manager.init_app(app); login_manager.login_view = "main.login"
    from .models import User
    @login_manager.user_loader
    def load_user(user_id): return db.session.get(User, int(user_id))
    from .routes import bp
    app.register_blueprint(bp)
    @app.context_processor
    def globals_for_templates(): return {"adsense_client_id": app.config["ADSENSE_CLIENT_ID"]}
    @app.errorhandler(404)
    def missing(_): return render_template("error.html", code=404, title="Page not found", message="The page you requested doesn’t exist or has moved."), 404
    @app.errorhandler(500)
    def failure(_):
        db.session.rollback()
        return render_template("error.html", code=500, title="Something went wrong", message="Our team has been notified. Please try again shortly."), 500
    with app.app_context():
        db.create_all()
        from .seed import seed
        seed()
    return app
