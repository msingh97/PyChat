import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	username = Column(String(11), primary_key=True)

class Message(Base):
	__tablename__ = "messages"

	time = Column(Float, primary_key=True)
	user = Column(String(11), ForeignKey("users.username"))
	message = Column(String, nullable = False)

engine = create_engine("sqlite:///chatroom.db")
Base.metadata.create_all(engine)