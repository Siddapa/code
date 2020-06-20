from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.models import User, Post
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    index_user = User.query.filter_by(username=current_user.username).first()
    completed_list = []
    for index_post in Post.query.filter_by(post_user=current_user.username):
        using_post = index_post.body
        broken_list = []
        string_list = []
        walker = 0
        wrapped_string = ""
        for character in using_post:
            if len(using_post) < 36:
                broken_list.append(using_post)
                break
            if walker >= 36:
                for character2 in string_list:
                    wrapped_string = wrapped_string + character2
                broken_list.append(wrapped_string)
                using_post = using_post.replace(wrapped_string, "", 1)
                walker = 0
                wrapped_string = ""
                string_list = []
            string_list.append(character)
            walker += 1
        completed_list.append(broken_list)
    return render_template('login.html', title='Home', Post=Post, user=index_user, completed_list=completed_list)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post_post = Post.query.filter_by(heading=form.heading.data).first()
        if post_post is not None:
            flash('Duplicate Title')
            return redirect(url_for('post'))
        form_heading = form.heading.data
        form_body = form.body.data
        new_post = Post(post_user=current_user.username, heading=form_heading, body=form_body)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user_routes = User.query.filter_by(username=form.username.data).first()
        if login_user_routes is None or not login_user_routes.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(login_user_routes, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/all_users')
def all_users():
    usernames = [User.username for user in User.query.all()]
    users = User.query.all()
    html_code = """
    {% extends 'base.html' %}
    
    {% block content %}
    <table>
        <tr> 
            <th>Username</th>
            <th>Email</th>
            <th>Last Seen</th>
            <th>Delete User </th>
        </tr>
    {% for row in users %}
        {% if row.username == "admin" %}
        {% else %}
            <tr> 
                <td> {{ row.username }} </td>
                <td> {{ row.email }} </td>
                <td> {{ row.last_seen }} </td>
                <form> 
                    <td>
                        <button type='submit' formaction="{{ url_for('delete_user', username=row.username) }}"> Delete {{ row.username }} </button>
                    </td>
                </form>
            </tr>
        {% endif %}
    {% endfor %}
    </table>
    {% endblock %}
    """
    with open('app/templates/all_users.html', 'w') as html_file:
        html_file.write(html_code)
    html_file.close()
    return render_template('all_users.html', users=users)


@app.route('/delete/<username>')
def delete_user(username):
    delete_user_user = User.query.filter_by(username=username).first()
    delete_username = delete_user_user.username
    db.session.delete(delete_user_user)
    db.session.commit()
    return render_template("delete_user.html", delete_username=delete_username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        register_user = User(username=form.username.data, email=form.email.data)
        register_user.set_password(form.password.data)
        db.session.add(register_user)
        db.session.commit()
        register_login = User.query.filter_by(username=form.username.data).first()
        login_user(register_login)
        redirect(url_for('user', username=form.username.data))
        flash('Congratulations, you are now a registered user!')
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user_user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user_user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # when submitted, the strings in the data boxes will be copied to the current user
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect('/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        # pre-inputting current user and about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    follow_user = User.query.filter_by(username=username).first()
    if follow_user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if follow_user == current_user:
        flash("You can't follow yourself!")
        return redirect(url_for('user', username=username))
    current_user.follow(follow_user)
    db.session.commit()
    flash('You are now following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    unfollow_user = User.query.filter_by(username=username).first()
    if unfollow_user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if unfollow_user == current_user:
        flash("You can't unfollow yourself!")
        return redirect(url_for('index'))
    current_user.unfollow(unfollow_user)
    db.session.commit()
    flash("You are not following {}".format(username))
    redirect(url_for('index'))
    return redirect(url_for('user', username=username))


@app.route('/meet_users')
@login_required
def meet_users():
    meet_user = User.query.all()
    curr = current_user.username
    return render_template('meet_users.html', list_of_users=meet_user, curr=curr)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
