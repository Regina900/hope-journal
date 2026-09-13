from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user

from config import Config
from database.database import db
from database.models import User

from routes.auth import auth
from routes.journal import journal
from routes.prayer import prayer
from routes.scriptures import scriptures
from routes.insights import insights
from routes.next_step import next_step

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register authentication routes
    app.register_blueprint(auth)
    app.register_blueprint(journal)
    app.register_blueprint(prayer)
    app.register_blueprint(scriptures)
    app.register_blueprint(insights)
    app.register_blueprint(next_step)
    
    # Home page
    @app.route("/")
    def index():
        return render_template("index.html")

    # Temporary dashboard
    @app.route("/dashboard")
    @login_required
    def dashboard():

        return render_template(
            "dashboard.html",
            username=current_user.username
        )

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)