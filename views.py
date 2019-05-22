from models import Base, User, Category, Book
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash

#SQLALCHEMY ORM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc

import json, random, string, os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import requests
from flask import make_response, session as login_session

engine = create_engine('sqlite:///library.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

APPLICATION_NAME = "Library"

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret. It has to be stored in the app root dir
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for all personal info, including any personal info you've made publicly available"
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
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

@app.route('/revoke')
def revoke():
  if 'credentials' not in login_session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **login_session['credentials'])

  revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

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

@app.route('/')
@app.route('/library')
def showLibrary():

    categories = session.query(Category).all()
    recentBooks = session.query(Book).order_by(desc(Book.created_date)).limit(10).all()

    if 'credentials' not in login_session:
        return render_template('public_library.html',categories = categories, recent_books = recentBooks)

    else:
      # Load credentials from the session.
      credentials = google.oauth2.credentials.Credentials(
        **login_session['credentials'])

       # Get user info
      userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
      params = {'access_token': credentials.token, 'alt': 'json'}
      answer = requests.get(userinfo_url, params=params)

      data = answer.json()

      login_session['username'] = data['name']
      login_session['picture'] = data['picture']
      login_session['email'] = data['email']

       # see if user exists, if it doesn't make a new one
      user_id = getUserID(data["email"])
      if not user_id:
          user_id = createUser(login_session)
      login_session['user_id'] = user_id

      user = session.query(User).filter_by(email=data['email']).one()

      return render_template('private_library.html',categories = categories, recent_books = recentBooks, user = user)

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
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
    category = session.query(Category).filter_by(id = category_id).one()
    booksForCategory = session.query(Book).filter_by(category_id = category_id).all()

    if 'username' not in login_session:
        return render_template('public_books.html', category = category, books_for_category = booksForCategory)
    else:
      user= session.query(User).filter_by(email=login_session['email']).one()
      booksOfUser = session.query(Book).filter_by(user_id = user.id, category_id = category_id).all()
      print(booksOfUser)
      return render_template('private_books.html', category = category, books_for_user = booksOfUser, user = user)

@app.route('/library/<int:category_id>/<int:book_id>')
def showBook(category_id, book_id):
    book = session.query(Book).filter_by(book_id = book_id).one()
    category =  session.query(Category).filter_by(id = category_id).one()
    return render_template('book.html', book = book, category = category)

@app.route('/library/add_book', methods=['GET', 'POST'])
def addBook():
    if 'username' not in login_session:
      return redirect(url_for('authorize'))

    if request.method == 'POST':
        category = session.query(Category).filter_by(name = request.form['category']).one()
        categoryID = category.id

        newBook = Book(
          title=request.form['title'],
          author=request.form['author'],
          location = request.form['location'],
          category_id = categoryID,
          user_id=login_session['user_id']
          )

        session.add(newBook)
        flash('New Book %s Successfully Created' % newBook.title)
        session.commit()
        return redirect(url_for('showLibrary'))
    else:
      return render_template('add_book.html', user_name = login_session['username'])

@app.route('/library/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
  if 'username' not in login_session:
      return redirect(url_for('authorize'))
  return render_template('edit_book.html')


@app.route('/library.json')
def libraryJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])

@app.route('/library/<int:category_id>/books.json')
def booksInCategoryJSON(category_id):
    books = session.query(Book).filter_by(category_id = category_id).all()
    return jsonify(Book=[b.serialize for b in books])


@app.route('/library/<int:id>/booksOfUser.json')
def booksOfUserJSON(id):
    books = session.query(Book).filter_by(user_id = id).all()
    return jsonify(Book=[b.serialize for b in books])

@app.route('/library/<int:category_id>/<int:book_id>/book.json')
def bookJSON(category_id, book_id):
    book = session.query(Book).filter_by(category_id = category_id, book_id = book_id).one()
    return jsonify(Book=book.serialize)


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
