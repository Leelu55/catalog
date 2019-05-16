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



engine = create_engine('sqlite:///library.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route("/")
@app.route("/library")
def showCategoresAndRecentBooks():
    return "Hello World!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
