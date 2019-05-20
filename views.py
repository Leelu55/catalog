from models import Base, User, Category, Book
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash

#SQLALCHEMY ORM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

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
# information for this application, including its client_id and client_secret.
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
  return redirect(url_for('showCategoresAndRecentBooks'))

@app.route('/')
@app.route('/library')
def showCategoresAndRecentBooks():

    if 'credentials' not in login_session:
        return redirect('authorize')

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

    categories = session.query(Category).all()
    recentBooks = session.query(Book).limit(2).all()
    return render_template('library.html',categories = categories, recent_books = recentBooks)



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
    return render_template('books.html', category = category, books_for_category = booksForCategory)

@app.route('/library/<int:category_id>/<int:book_id>')
def book(category_id, book_id):
    book = session.query(Book).filter_by(book_id = book_id).one()
    category =  session.query(Category).filter_by(id = category_id).one()
    return render_template('book.html', book = book, category = category)

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
