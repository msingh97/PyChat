from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, User


engine = create_engine('sqlite:///chatroom.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/")
def home_screen():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		user = session.query(User).filter_by(username=username, password=password).first()

		if not user:
			# If the given username and password don't exist in the database
			flash("Incorrect username or password. Please try again.")
			return redirect(url_for('login'))
		return redirect(url_for(chatroom, username=username, password=password))
	return render_template("login.html")

@app.route("/chatroom")
def chatroom(username, password):
	#chatroom here.



if __name__ == "main":
	app.debug = True
	app