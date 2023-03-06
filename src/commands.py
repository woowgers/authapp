import click
from flask import current_app

from flask_bcrypt import generate_password_hash
from db import DBCursorContext, ModelError

from tabulate import tabulate
from getpass import getpass

from db.operations.user import db_add_admin, db_delete_user_by_email, db_get_admins


@click.command("create-admin", help="Register a new admin")
@click.argument("email")
@click.argument("username")
def create_admin(email, username):
    password = getpass("Password: ")
    if not all((email, username, password)):
        click.echo(click.style("Failed to add administrator: All fields are required", fg="red"))
        return

    pw_hash = generate_password_hash(password)

    with DBCursorContext(current_app.config['DATABASE']) as db:
        try:
            db_add_admin(db, email, username, pw_hash)
        except ModelError as error:
            click.echo(click.style(f"Failed to add administrator: It is likely that a user with such email already exists.\n{error}", fg="red"))


@click.command("delete-admin", help="Unregister admin")
@click.argument("email")
def delete_admin(email):
    with DBCursorContext(current_app.config['DATABASE']) as db:
        db_delete_user_by_email(db, email)
        if db.rowcount == 0:
            click.echo(
                click.style(f"Failed to delete administrator: Could not find administrator with specified email.", fg="red")
            )


@click.command("list-admins", help="List registered admins")
def list_admins():
    with DBCursorContext(current_app.config['DATABASE']) as db:
        admins = db_get_admins(db)
        if len(admins) > 0:
            click.echo(f"Have {len(admins)} admin(s):")
            headers = ("USERNAME", "EMAIL", "ID", "USER_TYPE", "PW_HASH")
            table = map(str, admins)
            click.echo(tabulate(table, tablefmt="fancy_grid", headers=headers))
        else:
            click.echo("No admins have found.")

