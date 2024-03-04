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
        # Information for Admin
        username = request.form['username']
        password = request.form['password']
        # Information for Employee
        firstName = request.form['Employee First Name']
        lastName = request.form['Employee Last Name']
        Salary = request.form['Salary']
        Gender = request.form['Gender']
        DOB = request.form['Date of Birth']
        Manager = request.form['Manager']
        JobSite = request.form['JobSite']

        db = get_db()
        error = None

        if not username:
            error = 'Username required.'
        elif not password:
            error = 'Password required'
        elif user_type not in ['admin', 'employee']:
            error = 'Invalid user type'

        if error is None:
            try:
                if user_type == 'admin':
                    db.execute(
                        "INSERT INTO Admin (Username, Password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                elif user_type == 'employee':
                    db.execute(
                        "INSERT INTO Employee (Username, Password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (firstName, lastName, Salary, Gender, DOB, Manager, JobSite)
                    )
                db.commit()
            except db.IntegrityError:
                if user_type == 'admin':
                    error = f"Administrator {username} is already registered."
                elif user_type == 'employee':
                    error = f"Employee {firstName, ' ', lastName} is already registered."
            else:
                return redirect(url_for("sites.index"))
            flash(error)
    return render_template('sites/register.html')


@bp.route('/create')
@login_required
def create():
    db = get_db()
    if request.method == 'POST':
        error = None

        db.execute(

        )
