
# Collective Library

[Full Stack Web Developer Nanodegree](https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004) task **The Item Catalog** Task:
The **catalog** web app written in Python, HTML, CSS and Javascript provides lists of books within book categories like fiction or poetry, using Google Oauth 2.0 as a user registration and authentication system. Logged-in users can add, edit and delete books.

### Prerequisites

- **Python 2.7 Python**

Check version with:
```
python --version
```
If you haven't Python installed yet, download it [here](https://www.python.org/downloads/release/python-2716/) and follow installation instructions.

- **pip package installer for Python**
```
  pip install pip
```
- **SQLAlchemy Toolkit and ORM**

[Download and Installation Instructions](https://docs.sqlalchemy.org/en/13/intro.html)
```
pip install SQLAlchemy
```

- **Flask Python web framework**

[Download and Installation Instructions](http://flask.pocoo.org/docs/1.0/installation/#installation)
```
  pip install pip
```

- **Materialize CSS**
[Download and Installation Instructions](https://materializecss.com/getting-started.html)


- **Google Account**

Get an Account [here](https://accounts.google.com/signup/v2/webcreateaccount?service=cloudconsole&continue=https%3A%2F%2Fconsole.developers.google.com%2Fapis%2Fcredentials%2Foauthclient%2F757126685548-746rj9atg5nu6tsf0ouj2hcr7vpva5dn.apps.googleusercontent.com%3Fproject%3Dlibrary-240907%26hl%3Dde%26organizationId%3D56443648637&hl=de&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp&nogm=true)

- **Google OAuth 2.0 for Server-side Web Apps**
```
 pip install --upgrade google-api-python-client
```

Obtain Google authorization credentials following these [instructions](https://developers.google.com/identity/protocols/OAuth2WebServer#enable-apis)
Place the client_secrets.json file in the main directory of the project ("/catalog").

## Getting Started

1. Install all [prerequisites](https://github.com/Leelu55/catalog#prerequisites)

2. Run the initializer script to create the database and populate it with test data

```
python lotsof_books_categories.py
```

3. Run the application

```
python views.py
```

4. Visit http://localhost:8000

5. For using the authorized-user-only features like editing, deleting and adding books, **login** using your Google account.

6. Image upload is not yet implemented.
For adding images to new books, place these in the /statics/images folder and use their file names in the book image input field

## Built With

* [SQLAlchemy](https://www.sqlalchemy.org/) - Toolkit and ORM
* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Materialize](https://materializecss.com/) - CSS Framework
* [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/) - OAuth Provider

## Authors

* **[[Maria]](https://github.com/Leelu55/)**

See also the list of [contributors](https://github.com/Leelu55/catalog/contributors) who participated in this project.

## Acknowledgments

* Inspirations : Full Stack Web Developer Nanodegree code


