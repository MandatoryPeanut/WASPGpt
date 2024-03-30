from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash

from .auth import login_required
from .db import get_db

bp = Blueprint('sites', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    jobSites = db.execute(
        "SELECT id, Name FROM JobSite ORDER BY id;"
    ).fetchall()

    Admins = db.execute(
        "SELECT Username FROM Admin ORDER BY id;"
    ).fetchall()

    Taxes = db.execute(
        "SELECT Amount, Description, Date, Category FROM Taxes ORDER BY id;"
    ).fetchall()

    return render_template('sites/index.html', jobSites=jobSites, Admins=Admins, Taxes=Taxes)


@bp.route('/register/<string:user_type>', methods=['GET', 'POST'])
@login_required
def register(user_type):
    if request.method == 'POST':
        user_type = request.form['user_type']
        error = None
        if user_type == 'admin':
            # Information for Admin
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Username required.'
            elif not password:
                error = 'Password required'

            if error is None:
                db = get_db()
                try:
                    db.execute(
                        "INSERT INTO Admin (Username, Password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"Administrator {username} is already registered."
                    flash(error)
            else:
                return redirect(url_for("sites.index"))

        elif user_type == 'employee':
            # Information for Employee
            firstName = request.form['Employee First Name']
            lastName = request.form['Employee Last Name']
            Salary = request.form['Salary']
            Gender = request.form['Gender']
            DOB = request.form['Date of Birth']
            Manager = request.form['Manager']
            JobSite = request.form['JobSite']

            if not firstName or not lastName or not Salary or not Gender or not DOB or not Manager or not JobSite:
                error = 'You are missing one or more important fields of information.'
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO Employee (EmployeeFirstName, EmployeeLastName, Salary, Gender, DOB, Manager, JobSite) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (firstName, lastName, Salary, Gender, DOB, Manager, JobSite)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Employee {firstName, ' ', lastName} is already registered."
            else:
                return redirect(url_for("sites.index"))

        elif user_type == 'manager':
            # Information for Manager
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Username required.'
            elif not password:
                error = 'Password required'

            if error is None:
                db = get_db()
                try:
                    db.execute(
                        "INSERT INTO Manager (Username, Password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"Manager {username} is already registered."
                    flash(error)
            else:
                return redirect(url_for("sites.index"))

        elif user_type == 'job-site':
            Name = request.form['Name']
            db = get_db()
            existing_site = db.execute("SELECT Name FROM JobSite WHERE Name = ?;", (Name,)).fetchone()
            if existing_site is not None:
                error = f"Job Site with the name {Name} already exists."
                flash(error)
            else:
                db.execute("INSERT INTO JobSite (Name) VALUES (?);", (Name,))
                db.commit()
                flash("Job Site successfully created.")
                return redirect(url_for("sites.index"))
        if error is None:
            flash("Registration successful.")
            return redirect(url_for("sites.index"))

    return render_template('sites/register.html', user_type=user_type)


@bp.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        Name = request.form['Name']
        error = None
        db = get_db()
        existing_site = db.execute("SELECT Name FROM JobSite VALUES ?;", (Name,))
        if existing_site is not None:
            error = f"Job Site with the name {Name} already exists."
            flash(error)
        else:
            db.execute("INSERT INTO JobSite VALUES ?;", (Name,))
            db.commit()
            flash("Job Site successfully created.")
            return redirect(url_for("sites.index"))
    else:
        return render_template('sites/create.html')


@bp.route('/display/<int:jobSiteID>', methods=['GET'])
@login_required
def display(jobSiteID):
    db = get_db()
    Name = db.execute(
        "SELECT Name FROM JobSite WHERE id = ?;", (jobSiteID,)
    ).fetchone()
    Employees = db.execute(
        "SELECT * FROM Employee JOIN JobSite ON JobSite.id = Employee.JobSite WHERE Employee.JobSite = ?;", (jobSiteID,)
    ).fetchall()
    Income = db.execute(
        "SELECT * FROM Income JOIN JobSite ON JobSite.id = Income.JobSite WHERE Income.JobSite = ?;", (jobSiteID,)
    ).fetchall()
    Expenditure = db.execute(
        "SELECT * FROM Expenditure JOIN JobSite ON JobSite.id = Expenditure.JobSite WHERE Expenditure.JobSite = ?;",
        (jobSiteID,)
    ).fetchall()
    return render_template(
        'sites/display.html', Employees=Employees, Income=Income,
        Expenditure=Expenditure, jobSiteID=jobSiteID, Name=Name)
