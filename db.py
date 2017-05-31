import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String(11), nullable=False)

class Message(Base):
	__tablename__ = "messages"

	id = Column(Integer, primary_key=True)
	time = Column(String, nullable=False)
	user = Column(String(11), ForeignKey("users.username"))
	message = Column(String, nullable = False)

engine = create_engine("sqlite:///chatroom.db")
Base.metadata.create_all(engine)