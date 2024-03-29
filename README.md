# [DIY Catalogue](http://d-i-y.herokuapp.com/)

D-I-Y is a online catalogue of home crafts, creations lifstyle and heatlh projects, with step by step tutorials on how to create different items in and around the home, or even something to better yourself.
Featuring unique user logins and editable step by step guides.

## UX

The purpose of this project is to provide a platform for creative, diy and fitness enthusiasts to share their projects with other people. Allowing people to see their work and create things along with the creator, and achieve their own take on the project submitted by someone else.

Allowing users to sign up with an account and submit projects containg difficulty levels, steps by steps instructions, materials needed and a description of what they  have submitted.

Making use of the Flask micro-framework and MongoDB to store information

[Part 1](doc/part1.jpg)
[Part 2](doc/part2.jpg)
[Part 3](doc/part3.jpg)

Link to the [Live Site](http://d-i-y.herokuapp.com/)

## Features

### Existing Features

User account creation.
    - User will be able to sign up with their own account, filling in a sign up form to register, login in to the site when they return and login out when they leave.

Project submission to the catalogue

- The ability to create and upload a project to the database. The user will fill out and submit a form to complete this, containing text and image data.

View a project

- The main purpose of the site, to view the projects created. A main paginated dashboard will be displayed, and then a user can load a specific project they would like to view.

Edit project information

- Ability to make changes to your own projects, but not be able to access other users projects and edit or delete them. This will be achieved by requesting the specific data form the database and displaying it in the same form to edit it.

Delete a project

- Users will have the option to delete their own projects.

User profile
    - Somewhere users can see content from one user, and somewhere similar the user can see all their projects submitted, to easily manage them.

### Features Left to Implement

Filtering displayed projects
    - Allow the user to filter the project by category or creator

## Technologies Used

[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) | [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | [Jquery](https://jquery.com/)

[Masonary Grid](https://masonry.desandro.com/) | [ImageLoaded](https://masonry.desandro.com/)

[Python](https://www.python.org/) | [MongoDB](https://www.mongodb.com/)

[Material CSS](https://materializecss.com/) | [Flask](https://flask.palletsprojects.com/en/1.0.x/) | [Pymongo](https://api.mongodb.com/python/current/)

[Flask-Login](https://flask-login.readthedocs.io/en/latest/) | [flask-paginate](https://pythonhosted.org/Flask-paginate/) | [werkzeug](https://palletsprojects.com/p/werkzeug/)

[flask_wtf](https://flask-wtf.readthedocs.io/en/stable/) | [wtforms](https://wtforms.readthedocs.io/en/stable/)

## Testing

The application has been to tested to work well on desktop, tablet and mobile devices.

Further automated testing as been completed using PyTest and Flask-Pytest libraries. These automated tests run to ensure the endpoints of the application are being called correctly, adn the application reaches the correct destination.

To run these test, ensure you have installed the application locally following the guide below, and then run the following command in the development environment

```bash
pytest
```

This will automatically run the test found in test_app.py

The tests will run and complete will all tests passing.

## Deployment

The project is deployed with Heroku Platform using the Gunicorn production server, version control mangaged by GitHub, ensuring there are no development tools or processes running on the live version of the app.
Heroku will automattically update the running up form teh master branch of the application of GitHub, ensuring that lastest updates are always ready for users, once tested.

### To run this project locally

The application is run from a single app file (app.py).

- Ensure the following are installed

  - Python 3, programming language
  - PIP, python package manager

- Clone or Fork this repo

- navigate to the porject folder in your terminal of choice

- Install a local development server:
  - MAC

  ```bash
  python3 -m venv env
  ```

  - Windows

  ```bash
  python -m venv env
  ```

- Activate the environment
  - MAC

  ```bash
  source env/bin/activate
  ```

  - Windows

  ```bash
  env/Scripts/avtivate
  ```

- Install the requirments for the project to run

  ```bash
  pip install -r requirements.txt
  ```

- Rename the .env-dist file to .env

- Hook up a Mongo DB and create a secret key are need by the .env file

- Run the development server

  ```bash
  flask run
  ```

- The server will run on localhost:5000, unless otherwise tated in your terminal

- When you have finished with the server, do the following in the console the server is running

    To close the server

  ```bash
  ctrl + c
  ```

  To exit the virtual environment

  ```bash
  deactivate
  ```

### Bugs to fix

When adding a new step or material, then deleting it again, the counter does not take this into account and continues adding 

Deleting step 2 and then adding another step will add step 3, not 2.

## Credits

### Content

User created content and uploads.

### Media

- User uploaded media.

### Acknowledgements

- Pointers and guidance from [Mark Railton](https://www.markrailton.com/) (Mentor)

- Tutorial help with flask and login from [Pretty Printed](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)

- Tutorial help with uploading images safely [Julian Nash](https://www.youtube.com/channel/UC5_oFcBFlawLcFCBmU7oNZA)

- information from [Kirsten Hunter](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ) on LinkedIn Learning. A overview of flask and using logins, uploading images.
