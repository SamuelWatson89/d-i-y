import os
from flask import Flask, render_template, redirect, request, url_for, current_app, session, flash
from dotenv import load_dotenv
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.utils import secure_filename

app = Flask(__name__)
load_dotenv()
app.config["MONGO_DBNAME"] = 'diy'
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.secret_key = os.getenv('SECRET_KEY')
mongo = PyMongo(app)


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

    return render_template("projects.html",
                           projects=projects,
                           pagination=pagination,
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session['logged_in'] = True
    if "username" in session:
        return redirect(url_for("get_projects", username=session["username"]))
    return render_template('login.html')


@app.route("/login/<username>", methods=['GET', 'POST'])
def user(username):
    if request.method == "POST":
        username = session["username"]
        return redirect(url_for("user", username=session["username"]))
    return redirect(url_for("projects.html",
                            username=username,
                            ))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('get_projects'))


@app.route('/add_project')
def add_project():
    if "username" in session:
        return render_template('addproject.html', category=mongo.db.category.find())
    else:
        return redirect(url_for('login'))


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
            flash("AWESOME! You just submitted your project!")
            return redirect(url_for('get_projects'))


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/view_project/<projects_id>')
def view_project(projects_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    return render_template('viewproject.html',
                           projects=the_project)


@app.route('/edit_projects/<projects_id>')
def edit_projects(projects_id):
    the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    all_categories = mongo.db.category.find()
    if "username" in session:
        return render_template('editproject.html', projects=the_projects, category=mongo.db.category.find())
    else:
        return redirect(url_for('login'))


@app.route('/update_projects/<projects_id>', methods=["POST"])
def update_projects(projects_id):
    projects = mongo.db.projects
    projects.update({'_id': ObjectId(projects_id)},
                    {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
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
