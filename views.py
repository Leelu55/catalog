from models import Base, User, Category, Book
from flask import Flask, jsonify, request, url_for, abort, g, render_template

#SQLALCHEMY ORM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import json

#OAUTH IMPORTS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests



engine = create_engine('sqlite:///library.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
@app.route('/library')
def showCategoresAndRecentBooks():
    categories = session.query(Category).all()
    recentBooks = session.query(Book).limit(2).all()
    return render_template('library.html',categories = categories, recent_books = recentBooks)

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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
