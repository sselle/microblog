from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    user={'username': 'Sven'}
    posts=[
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Toy Story movie was so good!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # if user is already authenticated -> sent to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    # is TRUE, after clicking submit button and all validations in the form are ok
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # check if user is valid
        if user is None or not user.check_password(form.password.data):
            flash('User or PW are invalid')
            return redirect(url_for('login'))
        # login the user and redirect to index
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    # terminates the session handled from flask_login
    logout_user()
    return redirect(url_for('index'))