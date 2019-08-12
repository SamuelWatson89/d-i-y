
#DIY Catalogue

D-I-Y is a online catalogue of home crafts and creations, with step by step tutorials on how to create differnet items in and around the home, or even something to better yourself.
It will feature unique user logins and editable step by step guides.

## UX

Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:

- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.

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

### Features Left to Implement

Filtering displayed projects
    - Allow the user to filter the project by category or creator

User profile
    - Somewhere users can see content from one user, and somewhere similar the user can see all their projects submitted, to easily manage them.

## Technologies Used

[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)

[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)

[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

[Python](https://www.python.org/)

[MongoDB](https://www.mongodb.com/)


[Material CSS](https://materializecss.com/)

[Flask](https://flask.palletsprojects.com/en/1.0.x/)

[Pymongo](https://api.mongodb.com/python/current/)

[Flask-Login](https://flask-login.readthedocs.io/en/latest/)

[flask-paginate](https://pythonhosted.org/Flask-paginate/)

[werkzeug](https://palletsprojects.com/p/werkzeug/)

[flask_wtf](https://flask-wtf.readthedocs.io/en/stable/)

[wtforms](https://wtforms.readthedocs.io/en/stable/)


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

Project was deployed with Heroku Platform, version control manged by GitHub


This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:

- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.

## Credits

### Content

- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media

- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
