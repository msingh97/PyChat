import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	username = Column(String(11), primary_key=False)
	password = Column(String(11), nullable=False)
	# TODO: impletment logged_in column

engine = create_engine("sqlite:///chatroom.db")
Base.metadata.create_all(engine)