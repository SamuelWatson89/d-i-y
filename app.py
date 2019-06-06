import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'diy'
app.config["MONGO_URI"] = os.getenv(
    'MONGO_URI', 'mongodb+srv://Sam:MongoSam@myfirstcluster-odltf.mongodb.net/diy?retryWrites=true')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_projects')
def get_projects():
    return render_template("projects.html",
                           projects=mongo.db.projects.find())


@app.route('/add_project')
def add_project():
    return render_template('addproject.html',
                           category=mongo.db.category.find())


@app.route('/insert_project', methods=['POST'])
def insert_project():
    projects = mongo.db.projects
    projects.insert_one(request.form.to_dict())
    return redirect(url_for('get_projects'))


@app.route('/view_project/<projects_id>')
def view_project(projects_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    return render_template('viewproject.html',
                           projects=the_project)


@app.route('/edit_projects/<projects_id>')
def edit_projects(projects_id):
    the_projects = mongo.db.projects.find_one({"_id": ObjectId(projects_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editproject.html', projects=the_projects,
                           categories=all_categories)


@app.route('/update_projects/<projects_id>', methods=["POST"])
def update_projectsgit(projects_id):
    projects = mongo.db.projects
    projects.update({'_id': ObjectId(projects_id)},
                    {
        'title': request.form.get('title'),
        'category': request.form.get('categorye'),
        'description': request.form.get('description')
    })
    return redirect(url_for('get_projects'))


@app.route('/delete_project/<projects_id>')
def delete_project(projects_id):
    mongo.db.projects.remove({'_id': ObjectId(projects_id)})
    return redirect(url_for('get_projects'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
