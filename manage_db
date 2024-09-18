import click
from app import create_app
from db import db

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database has been reset and tables have been created.")
