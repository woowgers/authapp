from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
)

from proxies import db, user
from db import ModelError
from db.models import UserType
from db.operations.user import db_delete_user, db_get_user, db_get_users

from helpers.flashes import flash_error
from helpers.authority import login_required, admin_rights_required


bp = Blueprint("accounts", __name__, url_prefix="/accounts", template_folder="templates")


@bp.get("/")
@login_required
def root():
    if user.type == UserType.ADMIN.value:
        return redirect(url_for("accounts.all"))
    else:
        return redirect(url_for("accounts.me"))


@bp.get("/me/")
@login_required
def me():
    return render_template("nth.j2", user=user)


@bp.get("/all/")
@admin_rights_required
def all():
    return render_template("all.j2", users=db_get_users(db))


@bp.get("/<int:user_id>/")
@admin_rights_required
def nth(user_id: int):
    try:
        user = db_get_user(db, user_id)
    except ModelError as error:
        flash_error(error)
        return redirect(url_for("accounts.all"))

    return render_template("nth.j2", user=user)


@bp.post("/<int:user_id>/")
@admin_rights_required
def delete_nth(user_id: int):
    try:
        db_delete_user(db, user_id)
    except ModelError as error:
        flash_error(error)
        return redirect(url_for("accounts.all"))


@bp.post("/me/")
@login_required
def delete_me():
    try:
        db_delete_user(db, user.user_id)
    except ModelError as error:
        flash_error(error)
        return redirect(url_for("accounts.root"))

    return redirect(url_for("auth.logout"))

