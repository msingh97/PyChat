from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, User, Message
import time


engine = create_engine('sqlite:///chatroom.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		user = session.query(User).filter_by(username=username).first()

		if not user:
			# If the given username has not been logged in yet
			user = User(username=username)
			session.add(user)
			session.commit()
			return redirect(url_for("chatroom", username=username))
		else:
			flash("Someone has already logged in with username \"{0}\", please choose a different username.".format(username))
	return render_template("index.html")


@app.route("/chatroom/<string:username>/", methods=["GET", "POST"])
def chatroom(username):
	if not session.query(User).filter_by(username=username).all():
		# If there does not exist such a user
		return redirect(url_for("login"))
	if request.method == "POST":
		message_content = request.form["message_content"]
		if message_content:
			# ignore blank messages
			message_time = time.time()
			message = Message(time=message_time, user=username, message=message_content)
			session.add(message)
			session.commit()
			print("NEW MESSAGE -- " + username + ": " + message_content)
			all_messages = session.query(Message).order_by(Message.time)
			return redirect(url_for('chatroom', username=username))
	return render_template("chatroom.html", user=username, messages=session.query(Message).all(), to_string = to_string)

def to_string(time_float):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time_float))


if __name__ == "__main__":
	app.secret_key = "gneel"
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)