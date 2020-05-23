import os
import requests

from flask import Flask, session, request, render_template, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app, manage_session=False)

channels = [
    dict(name="GENERAL", messages=[])
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        session["username"] = request.form.get("username")
        return render_template("index.html")
    else:
        if "username" not in session:
            return render_template("username.html")
        else:
            return render_template("index.html")


@socketio.on("create channel")
def channel(data):
    if data["channel"] != "":
        channel = data["channel"].upper()
        if not existchannel(channel):
            channels.append(
                {
                    "name": channel,
                    "messages": []
                }
            )
    emit("channels", channels, broadcast=True)


@socketio.on("send message")
def channel(data):
    channel = data["channel"]
    message = data["message"]
    if message != "":
        addmessage(channel, message)

    emit("messages", channels, broadcast=True)


def existchannel(channel):
    for c in channels:
        if c["name"] == channel:
            return True
    return False


def getmessages(channel):
    for c in channels:
        if c["name"] == channel:
            return c["messages"]


def addmessage(channel, message):
    for c in channels:
        if c["name"] == channel:
            c["messages"].append({
                'sender': session.get("username") + ' - ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'text': message
            })

            if len(c["messages"]) > 100:
                c["messages"].pop(0)
