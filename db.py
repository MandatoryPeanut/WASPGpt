import sqlite3
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:  # g object stores data to be accessed by function requests
        g.db = sqlite3.connect(  # connects to database config
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # returns rows that behave like dicts

    return g.db


def close_db(e=None):  # checks if connection exist, if so its closed
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: # opens database relative to package
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
