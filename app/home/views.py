from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from forms import ResetAPIKeyForm
from ..models import User
from . import home
from .. import db
import uuid, sys

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/')
def homepage():
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('home/dashboard.html', user=user,title="Dashboard")

@home.route('/apikey/reset/<int:id>',methods=['GET','POST'])
@login_required
def reset_apikey(id):
    user = User.query.get_or_404(id)
    form = ResetAPIKeyForm(obj=user)
    if form.validate_on_submit():
        user.api_key = uuid.uuid4().hex
        db.session.add(user)
        db.session.commit()
        flash('You have successfully reseted the API Key.')
        return redirect(url_for('home.dashboard'))
    return render_template('home/resetapi.html',user=user, form=form, title='Reset API Key')


