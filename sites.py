from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('sites', __name__)


@bp.route('/')
@login_required
def index():  # gathers data for populating index html page
    db = get_db()
    jobSites = db.execute(
        "SELECT id, Name FROM JobSite ORDER BY id;"
    ).fetchall()

    Admins = db.execute(
        "SELECT Username FROM Admin ORDER BY id;"
    ).fetchall()

    Managers = db.execute(
        "SELECT Username FROM Manager ORDER BY id;"
    ).fetchall()

    Taxes = db.execute(
        "SELECT Amount, Description, Date, Category FROM Taxes ORDER BY id;"
    ).fetchall()

    return render_template('sites/index.html', jobSites=jobSites, Admins=Admins, Taxes=Taxes, Managers=Managers)


@bp.route('/register/<string:user_type>', methods=['GET', 'POST'])  # forms request fields for registration html page
@login_required
def register(user_type):
    sites = getSites()  # Data for listing sites
    if request.method == 'POST':
        user_type = request.form['user_type']
        error = None
        if user_type == 'admin':
            if session['user_status'] != 'admin':
                flash('You do not have permission to perform this action.')
                return redirect(url_for('index'))

            # Information for Admin
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            if not username:
                error = 'Username required.'
                if username == '':
                    error = 'Username cannot be empty spaces.'
            elif not password:
                error = 'Password required'
                if password == '':
                    error = 'Password cannot be empty spaces.'

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
                flash(error)
                return redirect(url_for("sites.index"))

        elif user_type == 'employee':
            # Information for Employee
            firstName = request.form['EmployeeFirstName'].strip()
            lastName = request.form['EmployeeLastName'].strip()
            Salary = request.form['Salary']
            Gender = request.form['Gender']
            DOB = request.form['DOB']
            Manager = request.form['Manager']
            JobSite = request.form['JobSite']

            if firstName == '':
                error = "Employees name cannot be empty."
            elif lastName == '':
                error = "Employees name cannot be empty."

            if error is None:

                db = get_db()
                existing_emp = db.execute(
                    "SELECT EmployeeFirstName, EmployeeLastName FROM Employee "
                    "WHERE EmployeeFirstName = ? AND EmployeeLastName = ?;", (firstName, lastName)
                ).fetchall()
                if existing_emp is None:
                    error = f"Employee {firstName, lastName} already exists."
                    flash(error)
                else:
                    db.execute(
                        "INSERT INTO Employee (EmployeeFirstName, EmployeeLastName, Salary, Gender, DOB, Manager, JobSite) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (firstName, lastName, Salary, Gender, DOB, Manager, JobSite)
                    )
                    db.commit()
                    flash("Employee registered successfully.")
                    return redirect(url_for("sites.index"))
            else:
                flash(error)
                return redirect(url_for("sites.index"))

        elif user_type == 'manager':
            if session['user_status'] != 'admin':
                flash('You do not have permission to perform this action.')
                return redirect(url_for('index'))

            # Information for Manager
            username = request.form['Manager-username'].strip()
            password = request.form['Manager-password'].strip()

            if not username:
                error = 'Username required.'
                if username == '':
                    error = 'Username cannot be empty spaces.'
            elif not password:
                error = 'Password required'
                if password == '':
                    error = 'Password cannot be empty spaces.'

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
                flash(error)
                return redirect(url_for("sites.index"))

        elif user_type == 'job-site':
            if session['user_status'] != 'admin':
                flash('You do not have permission to perform this action.')
                return redirect(url_for('index'))
            error = None
            Name = request.form['Name'].strip()

            if Name == '':
                error = "JobSite's name cannot be empty."

            if error is None:
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
            else:
                flash(error)
                return redirect(url_for("sites.index"))

        if error is None:
            flash("Registration successful.")
            return redirect(url_for("sites.index"))

    return render_template('sites/register.html', user_type=user_type, sites=sites)


@bp.route('/display/<int:jobSiteID>', methods=['GET', 'POST'])  # gathers information to populate display html page
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


@bp.route('/edit/<int:id>', methods=['POST', 'GET'])  # forms request fields for editing an Employee
@login_required
def edit(id):
    data = getEmployeeData(id)
    if request.method == 'POST':
        firstName = request.form['EmployeeFirstName'].strip()
        lastName = request.form['EmployeeLastName'].strip()
        Salary = request.form['Salary']
        Gender = request.form.get('Gender')
        DOB = request.form['DOB']
        Manager = request.form['Manager']
        error = None

        if not firstName or lastName =='':
            error = 'Employees name cannot be empty.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE Employee SET EmployeeFirstName = ?, EmployeeLastName = ?, Salary = ?, "
                "Gender = ?, DOB = ?, Manager = ? WHERE Employee.id = ?;",
                (firstName, lastName, Salary, Gender, DOB, Manager, id)
            )
            db.commit()
            flash("Update successful.")
            return redirect(url_for('sites.index'))
    return render_template('sites/edit.html', data=data)


def getEmployeeData(id):  # gets employees data
    data = get_db().execute(
        "SELECT * FROM Employee JOIN JobSite ON JobSite.id = Employee.JobSite WHERE Employee.id = ?;",
        (id,)
    ).fetchone()
    if data is None:
        abort(404, f"Employee {id} doesn't exist.")
    return data


def getSites():  # gets JobSites Name
    sites = get_db().execute(
        "SELECT * FROM JobSite;"
    ).fetchall()
    return sites


@bp.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete(id):  # deletes employee data
    db = get_db()
    db.execute("DELETE FROM Employee WHERE id = ?;", (id,))
    db.commit()
    return redirect(url_for('sites.index'))
