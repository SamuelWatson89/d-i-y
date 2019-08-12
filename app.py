import os
from flask import Flask, render_template, redirect, request, url_for, current_app, flash
from dotenv import load_dotenv
from flask_material import Material
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
load_dotenv()
app.config["MONGO_DBNAME"] = 'diy'
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.secret_key = os.getenv('SECRET_KEY')
mongo = PyMongo(app)
Material(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        object_id = self.username.get('_id')
        return str(object_id)

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    username = users.find_one({'_id': ObjectId(user_id)})
    return User(username)


class LoginForm(FlaskForm):
    username = StringField('<h6>Username &#128101;</h6>', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('<h6>Password &#128170;</h6>', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('<h6>remember me</h6>')


class RegisterForm(FlaskForm):
    email = StringField('<h6>Email Address &#128231;</h6> (valid email NOT required)', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('<h6>Username &#128101;</h6> (min 4 charaters)', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('<h6>Password &#128170;</h6> (min 8 charaters)', validators=[
                             InputRequired(), Length(min=8, max=80)])


@app.route('/')
@app.route('/get_projects')
def get_projects():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    offset = (page - 1) * per_page
    search = False
    q = request.args.get('q')
    if q:
        search = True

    projects = mongo.db.projects.find().sort('_id', pymongo.DESCENDING)[
        offset: offset + per_page]

    projects_to_render = projects.limit(per_page)

    pagination = Pagination(page=page, per_page=per_page,
                            total=projects.count(),
                            offset=offset,
                            search=search,
                            )
    if current_user.is_authenticated:
        return render_template('projects.html',
                               projects=projects,
                               pagination=pagination,
                               name=current_user.username)
    return render_template('projects.html',
                           projects=projects,
                           pagination=pagination)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user:
            if check_password_hash(user['password'], form.password.data):
                login_user(User(user))
                return redirect(url_for('get_projects'))
        flash('Sorry, that user does not exist')
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = ({"username": form.username.data,
                     "email": form.email.data,
                     "password": hashed_password})

        if mongo.db.users.count_documents({'username': form.username.data}, limit=1) != 0:
            flash('Username is taken, please choose another (sorry!)')
            return render_template('signup.html', form=form)
        elif mongo.db.users.count_documents({'email': form.email.data}, limit=1) != 0:
            flash(
                'Email address is already registered. Email support for assistance if needed.')
            return render_template('signup.html', form=form)
        else:
            mongo.db.users.insert_one(new_user)
            flash('Thank you for signing up!')
            return redirect(url_for('get_projects'))
    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_projects'))


@app.route('/add_project')
@login_required
def add_project():
    return render_template('addproject.html', category=mongo.db.category.find(), name=current_user.username)


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/insert_project', methods=['GET', 'POST'])
def insert_project():
    if request.method == "POST":
        if request.files:
            project_image = request.files['project_image']

            if project_image.filename == "":
                print("Image must have a name")
                flash("Image must have a name")
                return redirect(url_for('add_project'))

            if not allowed_image(project_image.filename):
                print("That image extension is not allawed")
                flash("That image extension is not allawed")
                return redirect(url_for('add_project'))

            else:
                filename = secure_filename(project_image.filename)
                mongo.save_file(project_image.filename, project_image)

            projects = mongo.db.projects
            projects.insert_one(request.form.to_dict())
        flash(
            "AWESOME! You just submitted your project!")
        return redirect(url_for('get_projects'))


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/view_project/<projects_id>')
def view_project(projects_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    if current_user.is_authenticated:
        return render_template('viewproject.html',
                               projects=the_project, name=current_user.username)
    return render_template('viewproject.html',
                           projects=the_project)


@app.route('/edit_projects/<projects_id>')
@login_required
def edit_projects(projects_id):
    the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    all_categories = mongo.db.category.find()

    return render_template('editproject.html', projects=the_projects, category=mongo.db.category.find(), name=current_user.username)


@app.route('/update_projects/<projects_id>', methods=["POST"])
def update_projects(projects_id):
    projects = mongo.db.projects
    projects.update({'_id': ObjectId(projects_id)},
                    {
        'title': request.form.get('title'),
        'creator': request.form.get('creator'),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'project_image_name': request.form.get('project_image_name'),
        'materials': request.form.get('materials'),
        'steps': request.form.get('steps')
    })
    return redirect(url_for('get_projects'))


@app.route('/delete_project/<projects_id>')
def delete_project(projects_id):
    mongo.db.projects.remove({'_id': ObjectId(projects_id)})
    return redirect(url_for('get_projects'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')))
