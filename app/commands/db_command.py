import os
import click
from app.extensions import db
from flask_migrate import upgrade, stamp
from app.seeders.seed_all import seed_all

def register_db_command(app):

    @app.cli.command("db:seed")
    def db_seed():
        seed_all()
        click.echo("Seeding selesai")

    @app.cli.command("db:fresh")
    def db_fresh():
        if os.getenv("FLASK_ENV") == "production":
            click.echo("Tidak boleh dijalankan di production!")
            return

        if not click.confirm("Yakin reset database?"):
            click.echo("Dibatalkan")
            return

        click.echo("Dropping all tables...")
        db.drop_all()

        click.echo("Reset migration state...")
        stamp(revision="base")

        click.echo("Running migration...")
        upgrade()

        click.echo("Seeding...")
        seed_all()

        click.echo("Database fresh + seed berhasil")