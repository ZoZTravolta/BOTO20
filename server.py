import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
from flask_cors import CORS
import string
import sqlite3
import uuid
import time
import datetime
import re


app = Flask(__name__)
CORS(app)


user = {
    "name": None,
    "is_todo": False,
    'askCreate': False,
}


@app.route("/")
def index():
    return render_template("index.html", user_name=user['name'])


def checkIfUserIsInDB(userName):
    connection = sqlite3.connect('botoBrain.db')
    curs = connection.cursor()
    curs.execute(f"SELECT * FROM users WHERE name = '{userName}' LIMIT 1")
    res = curs.fetchone()
    if res:
        user['id'] = res[0]
        return f"Good to see you again, {res[1]}"
    else:
        user['id'] = uuid.uuid1()
        curs.execute(
            f"INSERT INTO users VALUES ('{user['id']}' , '{userName}' )")
        connection.commit()
        return f"Welcome {user['name']}"


def createNewTask(user_message):
    connection = sqlite3.connect('botoBrain.db')
    task_id = uuid.uuid1()
    curs = connection.cursor()
    curs.execute(
        f"INSERT INTO tasks VALUES ('{task_id}', '{user['id']}','{user_message}',0,{time.time()})")
    connection.commit()


def readTodoList():
    connection = sqlite3.connect('botoBrain.db')
    curs = connection.cursor()
    curs.execute(
        f"SELECT * FROM tasks WHERE user_id = '{user['id']}'")
    user_tasks = curs.fetchall()
    new_res = ''
    for index, task in enumerate(user_tasks):
        if task[3] == 1:
            task_status = 'COMPLETED'
        else:
            task_status = 'INCOMPLETE'
        date = time.ctime(int(task[4]))
        date = str(date)
        new_res += f"{index+1}: Created at {date}: {task[2]} status: {task_status}  "
    return new_res


def updateTodoList(user_message):
    taskNum = int(re.search(r'\d+', user_message).group())

    connection = sqlite3.connect('botoBrain.db')
    curs = connection.cursor()
    curs.execute(
        f"SELECT * FROM tasks WHERE user_id = '{user['id']}' LIMIT 1 OFFSET {taskNum-1}")
    task = curs.fetchone()
    taskId = task[0]

    curs.execute(
        f"UPDATE tasks SET status = 1 WHERE id = '{taskId}' ")
    connection.commit()


@app.route('/todo/')
def todoFunc():

    user_message = request.args['message']

    if not user['name']:
        user['name'] = user_message
        return {"message": f"{checkIfUserIsInDB(user['name'])}, what would you like to do? create a new task or view your to do list?", "anim": "inlove.gif"}

    if "create" in user_message:
        user_message = user_message[7:]
        createNewTask(user_message)
        return {"message": "Created", "anim": "inlove.gif"}

    if 'read' in user_message:
        return {f"message": readTodoList(), "anim": "inlove.gif"}

    if 'update' in user_message:
        updateTodoList(user_message)
        return {"message": "Updated", "anim": "ok.gif"}

    return {"message": "todooooo", "anim": "inlove.gif"}


@app.route("/message/", methods=['GET'])
def get_message():
    user_message = request.args['message']
    if request.args.get('type'):
        Mtype = request.args['type']
    else:
        Mtype = 'from_external'

    if not user['name']:
        user['name'] = user_message
        return {"message": f"Hi, {user['name']}", "anim": "inlove.gif"}

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
        return {"message": "This is the bot police!! You are under arrest"}

    else:
        return {"message": "Hello world", "anim": "confused.gif"}


def drunk():
    connection = sqlite3.connect('botoBrain.db')
    curs = connection.cursor()
    curs.execute("SELECT * FROM drunk ORDER BY RANDOM() LIMIT 1")
    res = curs.fetchone()
    return res[1]


def trump():
    trumpQ = requests.get(
        'https://api.whatdoestrumpthink.com/api/v1/quotes/random').json()
    return trumpQ['message']


def external_bot(user_message):
    req = requests.get(
        f"https://morning-basin-34003.herokuapp.com/message/?message={user_message}").json()
    return req['message']


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
