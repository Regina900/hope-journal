from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from database.database import db
from database.models import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Basic validation
        if not username:
            flash("Please enter a username.", "error")
            return render_template("register.html")

        if not password:
            flash("Please enter a password.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash(
                "Password must be at least 8 characters long.",
                "error"
            )
            return render_template("register.html")

        # Check whether username already exists
        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash(
                "That username is already registered.",
                "error"
            )
            return render_template("register.html")

        # Create user
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(
            "Your account has been created. Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(url_for("dashboard"))

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("index"))