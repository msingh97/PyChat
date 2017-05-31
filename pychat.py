from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, User, Message
import time
import bleach


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
			user = User(id=num_users(), username=username)
			session.add(user)
			session.commit()
			return redirect(url_for("chatroom", user_id=user.id))
		else:
			flash("Someone has already logged in with username \"{0}\", please choose a different username.".format(username))
	return render_template("index.html")


@app.route("/chat/u/<int:user_id>/", methods=["GET", "POST"])
def chatroom(user_id):
	user = session.query(User).filter_by(id=user_id).first()
	if not user:
		# If there does not exist such a user
		return redirect(url_for("login"))
	if request.method == "POST":
		message_content = request.form["message_content"]
		if message_content:
			# ignore blank messages
			message_time = time_to_string()
			message_id = len(session.query(Message).all())
			message = Message(id = message_id, time=message_time, user=user.username, message=bleach.clean(message_content))
			session.add(message)
			session.commit()
			print("NEW MESSAGE -- " + user.username + ": " + message_content)
			all_messages = session.query(Message).order_by(Message.time)
			return redirect(url_for('chatroom', user_id=user_id))
	return render_template("chatroom.html", user=user, messages=session.query(Message).all(), users=num_users(), to_string = time_to_string)

@app.route("/chat/JSON")
def JSON():
	"""Returns all messages in JSON format."""
	return jsonify(Messages=messages_to_dict())

def messages_to_dict():
	"""Returns a list of dictionary objects representing each Message object in the database. To be used to 'jsonify' the message content."""
	return [{"time": i.time, "user": i.user, "message": i.message} for i in session.query(Message).all()]

def time_to_string():
	"""Converts time.time() object into a string."""
	Time = time.localtime()
	if Time.tm_hour >= 12:
		hour = str(Time.tm_hour - 12)
		post = "PM"
	else:
		hour = str(Time.tm_hour)
		post = "AM"
	if hour == "0":
		hour = "12"
	if Time.tm_min < 10:
		minute = "0" + str(Time.tm_min)
	else:
		minute = str(Time.tm_min)
	return hour + ":" + minute + " " + post

def num_users():
	"""The number of users in the database."""
	return len(session.query(User).all())

def clear_db():
	"""Deletes all messages and user entries in the database."""
	session.query(Message).delete()
	session.commit()
	session.query(User).delete()
	session.commit()
	print("\nDone.")

if __name__ == "__main__":
	try:
		app.secret_key = "gneel"
		app.debug = True
		app.run(host="0.0.0.0", port=5000)
	except KeyboardInterrupt:
		print("\nHalting server...")
	finally:
		clear_db()