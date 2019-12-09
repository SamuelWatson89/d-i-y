from flask import Flask, jsonify, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def get_projects():
        return jsonify(template='projects.html')

    
    @app.route('/login')
    def login():
        return jsonify(template='login.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)