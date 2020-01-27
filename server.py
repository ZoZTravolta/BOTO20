import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
import string
import sqlite3
# from models import Book


app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book_store.db"

# db = SQLAlchemy(app)


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     book_name = db.Column(db.String(40)) # ,  nullable=False
#     author = db.Column(db.String(30)) # , unique=True, nullable=False
#     year = db.Column(db.Integer) # , nullable=False
#     pic = db.Column(db.String(200), default="https://images-na.ssl-images-amazon.com/images/I/61-uFOBDLDL.jpg") # , nullable=False
#
#     def __repr__(self):
#         return f"Book('{self.book_name}')"
#
#


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message/", methods=['GET'])
def get_message():
    user_message = request.args['message']

    if request.args.get('type'):
        Mtype = request.args['type']
    else:
        Mtype = 'from_external'

    if Mtype == 'parrot':
        return {"message": user_message, "anim": "dog.gif"}

    if Mtype == 'broken':
        return {"message": "I'm so broken! I'm so broken...", "anim": "heartbroke.gif"}

    if Mtype == 'drunk':
        return {"message": drunk(), "anim": "dancing.gif"}

    if Mtype == 'trump':
        return {"message": trump(), "anim": "giggling.gif"}

    if Mtype == 'external-bot':
        return {"message": external_bot(user_message), "anim": "excited.gif"}

    if Mtype == 'from_external':
        return {"message": "This is the bot police! You are under arrest"}

    else:
        return {"message": "Hello world", "anim": "confused.gif"}


def drunk():
    connection = sqlite3.connect('botoBrain.db')
    curs = connection.cursor()
    curs.execute("SELECT * FROM drunk ORDER BY RANDOM() LIMIT 1")
    row = curs.fetchall()
    return row[0][1]


def trump():
    trumpQ = requests.get(
        'https://api.whatdoestrumpthink.com/api/v1/quotes/random').json()
    return trumpQ['message']


def external_bot(user_message):
    req = requests.get(
        f"https://boto20.herokuapp.com/message/?message={user_message}").json()
    return req['message']


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
