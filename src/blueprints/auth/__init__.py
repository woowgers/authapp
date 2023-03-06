from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from flask_bcrypt import check_password_hash, generate_password_hash

from proxies import db
from db import ModelError
from helpers.flashes import flash_error
from db.operations.user import db_add_user, db_get_user_by_email

from forms import LoginForm, RegisterForm


bp = Blueprint("auth", __name__, template_folder="templates")


@bp.get("/register/")
def register():
    return render_template("register.j2")


@bp.post("/register/")
def do_register():
    form = RegisterForm(request.form.to_dict())
    if not form.is_valid:
        return redirect(url_for("auth.register"))

    pw_hash = generate_password_hash(form.password)

    try:
        db_add_user(db, form.user_type, form.email, form.username, pw_hash)
    except ModelError as error:
        flash_error(error)
        return redirect(url_for("auth.register"))

    flash("You have successfully registered a new user!", category="success")
    return redirect(url_for("login"))


@bp.get("/login/")
def login():
    return render_template("login.j2")


@bp.post("/login/")
def do_login():
    form = LoginForm(request.form.to_dict())
    if not form.is_valid:
        return redirect(url_for("auth.login"))

    try:
        user = db_get_user_by_email(db, form.email)
    except ModelError as error:
        flash_error(error)
        return redirect(url_for("auth.login"))

    if not check_password_hash(user.pw_hash, form.password):
        flash_error("Invalid password.")
        return redirect(url_for("auth.login"))

    session['user'] = user
    return redirect(url_for("accounts.root"))

