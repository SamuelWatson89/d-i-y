# Import all required libraries
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
import hashlib

app = Flask(__name__)
load_dotenv()

# ? Connect to the Mongo Database
app.config["MONGO_DBNAME"] = 'diy'
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.secret_key = os.getenv('SECRET_KEY')
mongo = PyMongo(app)
Material(app)

# ? Define the flask_login manager.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ? Create the user class to handle user logins
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


# ? Load the login manager and get the users form the database
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    username = users.find_one({'_id': ObjectId(user_id)})
    return User(username)


# ? Create the form for the login page
class LoginForm(FlaskForm):
    username = StringField('<h6>Username &#128101;</h6>', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('<h6>Password &#128170;</h6>', validators=[
        InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me', description='Checkboxes can be tricky.')


# ? Create the form for the register page
class RegisterForm(FlaskForm):
    email = StringField('<h6>Email Address &#128231;</h6> (valid email NOT required)', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('<h6>Username &#128101;</h6> (min 4 charaters)', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('<h6>Password &#128170;</h6> (min 8 charaters)', validators=[
        InputRequired(), Length(min=8, max=80)])


# ? Landing page route, get the project from the database and set up pagination for them.
# ? If the user is logged in and authenticated, show the projects page.
@app.route('/')
@app.route('/get_projects')
def get_projects():
    '''
    Get all the projects form the database and prepare them for display.
    The results are paginated to 6 per page.
    '''
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    offset = (page - 1) * per_page
    search = False
    q = request.args.get('q')
    if q:
        search = True

    projects = mongo.db.projects.find().sort('_id', pymongo.DESCENDING)[
        offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page,
                            total=projects.count(),
                            offset=offset,
                            search=search,
                            )
    if current_user.is_authenticated:
        return render_template('projects.html',
                                projects=projects,
                                pagination=pagination,
                                name=current_user.username,
                                title="Welcome")
    return render_template('projects.html',
                            projects=projects,
                            pagination=pagination,
                            title="Welcome")


# ? Login page route, handles andauthenticates the user if the credentials are correct
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for the user to log in to the site and view their projects.
    Username and password will be validated to ensure they are logging in with
    the correct credentials.
    '''
    form = LoginForm()

    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user:
            if check_password_hash(user['password'], form.password.data):
                login_user(User(user), remember=form.remember.data)
                return redirect(url_for('get_projects'))
        flash('Sorry, that user does not exist')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form,
                            title="Login"
                            )


# ? Register page route, handles validation of username, email and password.
# ? If the details input already exist in the database, a flash message is shown with the error.
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    '''
    Created the sign up for and page for the user to register with the site
    User names and emails addresses will be vlaidated with what is already used,
    if email or username is used already, the user will be notified.
    '''
    if current_user.is_authenticated:  
        return redirect(url_for('add_project'))

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
            flash('Thank you for signing up! Login with your info to continue.')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form,
                            title="Sign up and get started"
                            )


# ? Log out route, terminate the users login session and return them to the homepage.
@app.route('/logout')
@login_required
def logout():
    '''
    Log the user out of the site, terminating their session
    '''
    logout_user()
    return redirect(url_for('get_projects'))


# ? Routing to direct the user to the create projet page.
@app.route('/add_project')
@login_required
def add_project():
    '''
    Take the user to the add project page provied they are logged in,
    otherwise take them to the sign in page
    '''
    return render_template('addproject.html', 
                            category=mongo.db.category.find(), 
                            name=current_user.username,
                            title="Submit a new project"
                            )


# ? Function to determine if uploaded files are allowed.
def allowed_image(filename):
    '''
    Determine if the file uploaded is an image.
    '''
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


# ? Route and functions to submit project to Mongo.
# ? If there are any issues with image supplied, a flash message will appear tell the user where they went wrong.
@app.route('/insert_project', methods=['GET', 'POST'])
def insert_project():
    '''
    Save the project to the database. Several checks made to ensure the filename is unique and
    the steps and materials are saved as an object (might not be the most effective solution, 
    but im happy to have figured this much out!).
    '''
    if request.method == "POST":
        if request.files:
            project_image = request.files['project_image']

            if project_image.filename == "":
                flash("Image must have a name")
                return redirect(url_for('add_project'))

            if not allowed_image(project_image.filename):
                flash("That image extension is not allowed")
                return redirect(url_for('add_project'))

            else:
                split = project_image.filename.rsplit(".", 1)
                temp_name = split[0]
                ext = "." + split[1]

                # ? Hash the image name so there are no duplicates
                hashed_name = hashlib.md5(temp_name.encode())
                hashed_file_name = hashed_name.hexdigest() + ext

                filename = secure_filename(hashed_file_name)
                mongo.save_file(filename, project_image)

            projects = mongo.db.projects
            project_dict = request.form.to_dict()
            update_image_name = {'project_image_name': filename}
            project_steps = {k:v for (k,v) in project_dict.items() if 'step' in k}
            project_materials = {k:v for (k,v) in project_dict.items() if 'material' in k}

            project_dict.update(update_image_name)
            project_dict['steps'] = project_steps
            project_dict['materials'] = project_materials
            projects.insert_one(project_dict)

        flash(
            "AWESOME! You just submitted your project!")

        return redirect(url_for('get_projects'))


# ? load the file on its own page if viewed directly (right click > open image in new tab).
@app.route('/file/<filename>')
def file(filename):
    '''
    View the image
    '''
    return mongo.send_file(filename)


# ? Routing and functions to get the project infomation from the database via the project ID
@app.route('/view_project/<projects_id>')
def view_project(projects_id):
    '''
    View the project and all its information.
    '''
    the_project = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    if current_user.is_authenticated:
        return render_template('viewproject.html',
                               projects=the_project,
                               name=current_user.username,
                               title="Project")
    return render_template('viewproject.html',
                           projects=the_project,
                           title="Project")


# ? Routine and functions to get the project ID form the database and allow the user to edit, provided its their project.
@app.route('/edit_projects/<projects_id>')
@login_required
def edit_projects(projects_id):
    '''
    Provided the user is logged in and owns the project, it can be edited.
    '''
    the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    all_categories = mongo.db.category.find()
    return render_template('editproject.html',
                           projects=the_projects,
                           category=all_categories,
                           name=current_user.username,
                           title="Edit Project")


# ? Update the project image on its own seperate page.
@app.route('/edit_image/<projects_id>')
@login_required
def edit_image(projects_id):
    '''
    Edit the image for the project on a seperate page
    '''
    the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    return render_template('editimage.html',
                           projects=the_projects,
                           name=current_user.username,
                           title="Edit Image")

# ? Routing and functions to update the databae collection with the new information provided
@app.route('/update_projects/<projects_id>', methods=["GET", "POST"])
def update_projects(projects_id):
    '''
    Take the changes the user has made to the project and update them in the database
    '''
    if request.method == "POST":
        projectTitle = request.form.get('title')
        projectCreator = request.form.get('creator')
        projectDescription = request.form.get('description')
        projectCatagory = request.form.get('category')
        projectMaterials = {k:v for (k,v) in request.form.items() if 'material' in k}
        projectSteps = {k:v for (k,v) in request.form.items() if 'step' in k}
        projectExperience = request.form.get('experience')

        projects = mongo.db.projects
        projects.update_one({'_id': ObjectId(projects_id)},
                        {
                            '$set' : {
                            'title': projectTitle,
                            'creator': projectCreator,
                            'description': projectDescription,
                            'category': projectCatagory,
                            'materials': projectMaterials,
                            'steps': projectSteps,
                            'experience': projectExperience
                            }
                        })
        the_project = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
        if current_user.is_authenticated:
            return render_template('viewproject.html',
                                projects=the_project,
                                name=current_user.username)
        return render_template('viewproject.html',
                            projects=the_project)


# ? Routing and functions to update the databae collection with the new information provided
@app.route('/update_image/<projects_id>', methods=["GET", "POST"])
def update_image(projects_id):
    '''
    Validate, hash the image name and upload the new image for the project.
    '''
    if request.method == "POST":
        if request.files:
            project_image = request.files['project_image']

            if project_image.filename == "":
                flash("Image must have a name")
                return redirect(url_for('add_project'))

            if not allowed_image(project_image.filename):
                flash("That image extension is not allowed")
                return redirect(url_for('add_project'))

            else:
                split = project_image.filename.rsplit(".", 1)
                temp_name = split[0]
                ext = "." + split[1]

                hashed_name = hashlib.md5(temp_name.encode())
                hashed_file_name = hashed_name.hexdigest() + ext

                filename = secure_filename(hashed_file_name)
                mongo.save_file(filename, project_image)

            projects = mongo.db.projects
            projects.update_one({'_id': ObjectId(projects_id)},
                            {
                                '$set' : {
                                'project_image_name': filename,
                                }
                            })
        the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
        all_categories = mongo.db.category.find()
        return render_template('editproject.html',
                                projects=the_projects,
                                category=all_categories,
                                name=current_user.username)


# ? Delete the project from the database
@app.route('/delete_project/<projects_id>')
def delete_project(projects_id):
    '''
    Let it go...
    '''
    mongo.db.projects.remove({'_id': ObjectId(projects_id)})
    return redirect(url_for('get_projects'))


# ? User profile page
@app.route('/view_profile/<user_id>')
def view_profile(user_id):
    '''
    Display the projects which the current logged in user has submitted
    '''
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    users_projects = mongo.db.projects.find()
    return render_template('userprofile.html',
                           name=current_user.username,
                           user=user,
                           users_projects=users_projects,
                           title="Users profile")

# ? About page
@app.route('/about')
def about():
    if current_user.is_authenticated:
        return render_template('about.html',
                                name=current_user.username,
                                title="About")
    return render_template('about.html',
                            title="About")


# ? Copntact page
@app.route('/contact')
def contact():
    if current_user.is_authenticated:
        return render_template('contact.html',
                                name=current_user.username,
                                title="Contact")
    return render_template('contact.html',
                            title="Contact")


# ? Route and functions to submit project to Mongo.
# ? If there are any issues with image supplied, a flash message will appear tell the user where they went wrong.
@app.route('/send_mail', methods=['GET', 'POST'])
def send_mail():
    if request.method == "POST":
        mail = mongo.db.mail
        mail_dict = request.form.to_dict()
        mail.insert_one(mail_dict)

        flash(
            "Thanks! Your mail has been posted.")

        return redirect(url_for('contact'))
        

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')))
