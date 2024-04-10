import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

from .chatgpt import sql_Test

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if sql_Test(username, password) == 0:
            db = get_db()
            error = None
            admin = db.execute(
                'SELECT * FROM Admin where Username = ?', (username,)
            ).fetchone()

            manager = db.execute(
                'SELECT * FROM Manager where Username = ?', (username,)
            ).fetchone()
            status = None

            if admin is not None:
                status = 'admin'
                if not check_password_hash(admin['password'], password):
                    error = 'Incorrect password'
            elif manager is not None:
                status = 'manager'
                if not check_password_hash(manager['password'], password):
                    error = 'Incorrect password.'
            else:
                error = 'User not found.'

            if error is None:
                session.clear()
                session['user_id'] = admin['id'] if admin else manager['id']
                session['user_status'] = status

                g.user_status = status
                return redirect(url_for('index'))

            flash(error)
        else:
            return render_template('auth/h4ck0r.html')
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_status = session.get('user_status')
    if user_id is None:
        g.user = None
    else:
        if user_status == 'admin':
            g.user = get_db().execute(
                'SELECT * FROM Admin WHERE id = ?', (user_id,)
            ).fetchone()
        elif user_status == 'manager':
            g.user = get_db().execute(
                'SELECT * FROM Manager WHERE id = ?', (user_id,)
            ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
