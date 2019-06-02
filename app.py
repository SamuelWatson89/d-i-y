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
@app.route('/get_tasks')
def get_tasks():
    return render_template("projects.html",
                           projects=mongo.db.projects.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
