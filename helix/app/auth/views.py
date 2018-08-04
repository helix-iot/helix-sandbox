from flask import abort, flash, redirect, render_template, url_for, session, request
from flask_login import login_required, login_user, logout_user
import uuid, os
from io import BytesIO
from . import auth
from forms import LoginForm, RegistrationForm, AdminSetupForm
from .. import db
from ..models import User

__author__ = "m4n3dw0lf"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    api_key=uuid.uuid4().hex
                   )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/admin_setup', methods=['GET', 'POST'])
def admin_setup():
    has_admin = User.query.filter_by(is_admin=True).first()
    if has_admin:
      abort(404)
    form = AdminSetupForm()
    if form.validate_on_submit():
        user = User(username="admin",
                    password=form.password.data,
                    api_key=uuid.uuid4().hex
                   )
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/admin_setup.html', form=form, title='Admin Setup')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,remember=True)
            session.permanent = True
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))
