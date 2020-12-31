from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from app.models import User

# executes right before any View function from Flask
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    #user={'username': 'Sven'}
    posts=[
        {
            'author': {'username': 'john'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'sven'},
            'body': 'The Toy Story movie was so good!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

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
        # redirect back to page requested after login
        next_page = request.args.get('next')
        # url_parse: security, to protect against malicious sites in next arguments
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    # terminates the session handled from flask_login
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you have successfully registered to Microblog!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    posts = [
        {'author': user, 'body': 'first dummy post'},
        {'author': user, 'body': 'second dummy post'}
    ]
    return render_template('user.html', user=user, posts=posts, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.username.about_me = current_user.about_me
    return render_template('edit_profile.html', title='Edit User Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))