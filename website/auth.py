from flask import Blueprint, render_template, request, flash, redirect, url_for
from email_validator import validate_email, EmailNotValidError
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm")

        valid_email = True
        password_error = password_authenticator(password)

        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            valid_email = False
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists, try logging in instead.", category="error")
        elif not valid_email:
            flash("Please enter a valid email.", category="invalid-input")
        elif password_error != 0:
            flash(f"Password is {password_error}.", category="invalid-input")
        elif password != password_confirm:
            flash("Passwords do not match.", category="invalid-input")
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method="pbkdf2:sha1"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/reset-password")
def reset_password():
    return render_template("home.html")


def password_authenticator(password: str):
    if len(password) < 8: return "too short"
    if not re.search(r"[a-z]", password): return "missing a lowercase letter"
    if not re.search(r"[A-Z]", password): return "missing an uppercase letter"
    if not re.search(r"\d", password): return "missing a number"
    if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>?]', password): return "missing a special character"

    return 0