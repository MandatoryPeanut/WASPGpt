import os.path
import sqlite3
import click
import json
from flask import current_app, g
from werkzeug.security import generate_password_hash


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
    with current_app.open_resource('wasp.sql') as f:  # opens database relative to package
        db.executescript(f.read().decode('utf8'))


def fill_db():  # Fills the database, with data found in json file
    db = get_db()

    with current_app.open_resource('db.json') as f:  # opens database relative to package
        currentData = json.loads(f.read())

    for table, records in currentData.items():
        if table == 'Admin':
            for data in records:
                username = data.get('Username')
                password = data.get('Password')
                # checks if user is registered or not
                existing_user = db.execute("SELECT id FROM Admin WHERE Username = ?", (username,)).fetchone()

                if existing_user is None:
                    db.execute(
                        "INSERT INTO Admin (Username, Password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                    db.commit()
                else:
                    print(f"User with username: {username} already exists.")

        elif table == 'Employee':
            for data in records:
                firstName = data.get('employeeFirstName')
                lastName = data.get('employeeLastName')
                Salary = data.get('Salary')
                Gender = data.get('Gender')
                DOB = data.get('DOB')
                manager = data.get('manager')
                jobSite = data.get('jobSite')

                existing_user = db.execute(
                    "SELECT id FROM Employee WHERE EmployeeFirstName = ? AND EmployeeLastName = ?;",
                    (firstName, lastName)).fetchone()
                if existing_user is None:
                    db.execute(
                        "INSERT INTO Employee (EmployeeFirstName, EmployeeLastName, Salary, Gender, DOB, Manager, JobSite) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (firstName, lastName, Salary, Gender, DOB, manager, jobSite)
                    )

        elif table == 'Expenditure':
            for data in records:
                amount = data.get('amount')
                description = data.get('description')
                date = data.get('date')
                category = data.get('category')
                jobSite = data.get('jobSite')

                db.execute(
                    "INSERT INTO Expenditure (Amount, Description, Date, Category, JobSite) VALUES (?, ?, ?, ?, ?)",
                    (amount, description, date, category, jobSite)
                )

        elif table == 'Income':
            for data in records:
                amount = data.get('amount')
                description = data.get('description')
                date = data.get('date')
                category = data.get('category')
                jobSite = data.get('jobSite')

                db.execute(
                    "INSERT INTO Income (Amount, Description, Date, Category, JobSite) VALUES (?, ?, ?, ?, ?)",
                    (amount, description, date, category, jobSite)
                )

        elif table == 'Taxes':
            for data in records:
                Amount = data.get('amount')
                Description = data.get('description')
                Date = data.get('date')
                Category = data.get('category')

                db.execute(
                    "INSERT INTO Taxes (Amount, Description, Date, Category) VALUES (?, ?, ?, ?)",
                    (Amount, Description, Date, Category)
                )


        elif table == 'JobSite':
            for data in records:
                JobSite = data.get('id')
                Name = data.get('Name')

                db.execute(
                    "INSERT INTO JobSite (Name) VALUES (?);",
                    (Name,)
                )
    db.commit()


def test_db():
    db = get_db()
    Admin = db.execute(
        "SELECT * FROM Admin;"
    ).fetchall()
    Employee = db.execute(
        "SELECT * FROM Employee;"
    ).fetchall()
    Expenditure = db.execute(
        "SELECT * FROM Expenditure;"
    ).fetchall()
    Income = db.execute(
        "SELECT * FROM Income;"
    ).fetchall()
    Taxes = db.execute(
        "SELECT * FROM Taxes;"
    ).fetchall()
    JobSite = db.execute(
        "SELECT * FROM JobSite;"
    ).fetchall()

    print("Admins:")
    for row in Admin:
        print(dict(row))
    print("\nEmployee:")
    for row in Employee:
        print(dict(row))
    print("\nExpenditure:")
    for row in Expenditure:
        print(dict(row))
    print("\nIncome:")
    for row in Income:
        print(dict(row))
    print("\nTaxes:")
    for row in Taxes:
        print(dict(row))
    print("\nJobSite:")
    for row in JobSite:
        print(dict(row))


@click.command('test-db')
def test_db_command():
    """Queries Database.."""
    test_db()
    click.echo('Finished queries.')


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


@click.command('fill-db')
def fill_db_command():
    """Inserts data into the database using the database file in the WASPGpt Database Folder."""
    fill_db()
    click.echo('Database filled.')


def test_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(test_db_command)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def fill_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(fill_db_command)
