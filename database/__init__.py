import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool

Base = declarative_base()

#this is defining the database models
class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    people = Column(String(250), ForeignKey('account.id'))


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    salt = Column(Integer, nullable=False)
    group = Column(String(250))
    groupId = Column(String(250), ForeignKey('group.id'))

class Todolist(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    group = Column(String(250), nullable=False)
    itemName = Column(String(250))
    itemContent = Column(String(250), nullable=False)

class AdminUsers(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    salt = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)

class Learn(Base):
    __tablename__ = 'learn'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    link = Column(String(250), nullable=False)
    groupId = Column(Integer, ForeignKey("group.id"))
    group = Column(String(250), nullable=False)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    ip = Column(String(250))
    endpoint = Column(String(250))

# this is the engine it is being run on the SingletonThreadPool to maintain thread 
engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
Base.metadata.create_all(engine)