from flask import Flask, jsonify, render_template, redirect, url_for


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def get_projects():
        return jsonify(template='projects.html')

    @app.route('/login')
    def login():
        return jsonify(template='login.html')

    @app.route("/signup")
    def signup():
        return jsonify(template='signup.html')

    @app.route("/add_project")
    def add_project():
        return jsonify(template='addproject.html')

    @app.route('/view_project/<projects_id>')
    def view_project(projects_id):
        return jsonify(template='viewproject.html')

    @app.route("/edit_project/<projects_id>")
    def edit_projects(projects_id):
        return jsonify(template='editproject.html')

    @app.route('/edit_image/<projects_id>')
    def edit_image(projects_id):
        return jsonify(template='editimage.html')

    @app.route("/about")
    def about():
        return jsonify(template='about.html')

    @app.route("/contact")
    def contact():
        return jsonify(template='contact.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
