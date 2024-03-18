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
                    "INSERT INTO Employee (Username, Password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (firstName, lastName, Salary, Gender, DOB, Manager, JobSite)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Employee {firstName, ' ', lastName} is already registered."
            else:
                return redirect(url_for("sites.index"))

        if error is None:
            flash("Registration successful.")
            return redirect(url_for("sites.index"))

    return render_template('sites/register.html', user_type=user_type)


@bp.route('/create')
@login_required
def create():
    db = get_db()
    if request.method == 'POST':
        error = None

        db.execute(

        )


@bp.route('/display/<int:jobSiteID>/<string:name>', methods=['GET'])
@login_required
def display(jobSiteID, name):
    db = get_db()
    Employees = db.execute(
        "SELECT * FROM Employee WHERE Employee.JobSite = ?;", (jobSiteID,)
    ).fetchall()
    Income = db.execute(
        "SELECT * FROM Income WHERE Income.JobSite = ?;", (jobSiteID,)
    ).fetchall()
    Expenditure = db.execute(
        "SELECT * FROM Expenditure WHERE Expenditure.JobSite = ?;", (jobSiteID,)
    ).fetchall()
    db.commit()
    return render_template(
        'sites/display.html', Employees=Employees, Income=Income,
        Expenditure=Expenditure, jobSiteID=jobSiteID, name=name)
