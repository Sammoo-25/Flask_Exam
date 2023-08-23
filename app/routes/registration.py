from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, login_required, logout_user

from .. import app
from ..models import Users
from ..forms import LoginForm, RegisterForm
from .. import db


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')

            next_page = session.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('userPage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    session['next'] = request.args.get('next')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = Users(name=form.name.data, surname=form.surname.data,
                         email=form.email.data, gender=form.gender.data, phone_number=form.phone_number.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('userPage'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
