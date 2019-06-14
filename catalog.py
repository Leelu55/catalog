# Import table Classes from database setup file (models.py)
from models import Base, User, Category, Book

# FLASK
from flask import Flask, request, url_for, abort, g, redirect
from flask import jsonify, render_template
from flask import make_response, session as login_session

# SQLALCHEMY ORM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy import create_engine, desc

# Google OAuth
import google.oauth2.credentials
import google_auth_oauthlib.flow

import requests
import json
import random
import string
import os

engine = create_engine('postgresql://catalog:library2019@localhost:5432/catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

APPLICATION_NAME = "catalog"

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and
# client_secret. It has to be stored in the app root dir
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__),
                                   'client_secrets.json')


# This OAuth 2.0 access scope allows for all personal info, including any
# personal info you've made publicly available"
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email']


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url()

    # Store the state so the callback can verify the auth server response.
    login_session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = login_session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    login_session['credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('showLibrary'))

# log out
@app.route('/revoke')
def revoke():
    if 'credentials' not in login_session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **login_session['credentials'])

    revoke = requests.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': credentials.token},
        headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return redirect(url_for('clear_credentials'))
    else:
        return('An error occurred.')


@app.route('/clear')
def clear_credentials():
    if 'credentials' in login_session:
        del login_session['credentials']
        login_session.clear()
    return redirect(url_for('showLibrary'))

# display main page
@app.route('/')
@app.route('/library')
def showLibrary():

    categories = session.query(Category).all()
    recentBooks = session.query(Book).order_by(
        desc(Book.created_date)).limit(6).all()

    pageTitle = "Library"
    if 'credentials' not in login_session:
        return render_template(
            'library.html',
            categories=categories,
            recent_books=recentBooks,
            page_title=pageTitle)

    else:
        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(
            **login_session['credentials'])

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()
        print(data)

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']

        # see if user exists, if it doesn't make a new one
        user_id = getUserID(data["email"])
        if not user_id:
            user_id = createUser(login_session)
        login_session['user_id'] = user_id

        user = session.query(User).filter_by(email=data['email']).one()

        return render_template(
            'library.html',
            categories=categories,
            recent_books=recentBooks,
            user=user,
            page_title=pageTitle)

# User Helper Functions


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        image=login_session['picture'])

    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/library/<int:category_id>/books')
def showBooksForCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    booksForCategory = session.query(Book).filter_by(
        category_id=category_id).all()
    pageTitle = category.name + " books"

    if 'username' not in login_session:
        return render_template(
            'books.html',
            category=category,
            books=booksForCategory,
            page_title=pageTitle,)
    else:
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        booksOfUser = session.query(Book).filter_by(
            category_id=category_id, user_id=user.id)

        return render_template(
            'books.html',
            category=category,
            books=booksForCategory,
            user_books=booksOfUser,
            user=user,
            page_title=pageTitle)


@app.route('/library/<int:category_id>/<int:book_id>')
def showBook(category_id, book_id):
    book = session.query(Book).filter_by(book_id=book_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    pageTitle = book.title
    bookImagePath = "images/" + book.image

    if 'username' not in login_session:
        return render_template(
            'book.html',
            book=book,
            category=category,
            page_title=pageTitle)
    else:
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        return render_template(
            'book.html',
            book=book,
            category=category,
            user=user,
            page_title=pageTitle)


@app.route('/library/add_book', methods=['GET', 'POST'])
def addBook():
    if 'username' not in login_session:
        return redirect(url_for('authorize'))

    if request.method == 'POST':
        category = session.query(Category).filter_by(
            id=request.form['category']).one()
        categoryID = category.id

        if request.form['image'] == "":
            imageString = "default_book.jpg"
        else:
            imageString = request.form['image']
        newBook = Book(
            title=request.form['title'],
            author=request.form['author_editor'],
            category_id=categoryID,
            description=request.form['description'],
            user_id=login_session['user_id'],
            image=imageString
        )

        session.add(newBook)
        session.commit()

        return redirect(url_for('showLibrary'))
    else:
        categories = session.query(Category).all()
        pageTitle = "Add new Book"
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        return render_template(
            'add_book.html',
            user=user,
            page_title=pageTitle,
            categories=categories)


@app.route('/library/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
    if 'username' not in login_session:
        return redirect(url_for('authorize'))

    book = session.query(Book).filter_by(book_id=book_id).one()

    if request.method == 'POST':

        if request.form['title']:
            book.title = request.form['title']
        if request.form['description']:
            book.description = request.form['description']
        if request.form['author']:
            book.author = request.form['author']
        if request.form['category']:
            book.category_id = request.form['category']
        if request.form['image'] != "":
            book.image = request.form['image']
        else:
            book.image = "default_book.jpg"

        session.add(book)
        session.commit()
        return redirect(url_for(
            'showBook', book_id=book.book_id, category_id=book.category_id))

    else:
        pageTitle = "Edit Book"
        categories = session.query(Category).all()

        return render_template(
            'edit_book.html',
            book=book,
            user_name=login_session['username'],
            page_title=pageTitle,
            categories=categories)


@app.route('/library/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(book_id):
    if 'username' not in login_session:
        return redirect(url_for('authorize'))
    bookToDelete = session.query(Book).filter_by(book_id=book_id).one()

    if request.method == 'POST':
        bookToDelete = session.query(Book).filter_by(book_id=book_id).one()
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showLibrary'))
    pageTitle = "Delete Book"
    return render_template(
        'delete_book.html',
        book=bookToDelete,
        user_name=login_session['username'],
        page_title=pageTitle)

# create a library dump with all categories and the related books
@app.route('/library.json')
def libraryJSON():

    cats = session.query(Category).options(joinedload(Category.books)).all()
    categories = [dict(c.serialize,
                       books=[b.serialize for b in c.books]) for c in cats]

    libraryDump = dict(categories=categories)

    return jsonify(libraryDump)


@app.route('/library/<int:category_id>/books.json')
def booksInCategoryJSON(category_id):
    books = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(Book=[b.serialize for b in books])


@app.route('/library/<int:id>/booksOfUser.json')
def booksOfUserJSON(id):
    books = session.query(Book).filter_by(user_id=id).all()
    return jsonify(Book=[b.serialize for b in books])


@app.route('/library/<int:category_id>/<int:book_id>/book.json')
def bookJSON(category_id, book_id):
    book = session.query(Book).filter_by(
        category_id=category_id, book_id=book_id).one()
    return jsonify(Book=book.serialize)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


if __name__ == '__main__':
    os.environ['DEBUG'] = '1'
    app.run()
