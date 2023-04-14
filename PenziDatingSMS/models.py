from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, time

from db_config import Base

class User(Base):
    __tablename__ = "user"

    # __table_args__ = (UniqueConstraint("phone_number"),)
    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))
    county = Column(String(100))
    town = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False, unique = True)
    date_registered = Column(DateTime, default = datetime.now )
    is_active = Column(Boolean, default=True)

    user_details= relationship("User_details", back_populates="owner", uselist=False)
    user_description = relationship("User_description", back_populates='owner', uselist=False)



class User_details(Base):
    __tablename__ = 'user_details'
    user_details_id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    level_of_education = Column(String(500), nullable=False)
    profession = Column(String(500))
    marital_status = Column(String(255))
    religion = Column(String(500))
    ethnicity = Column(String(500))
    phone_number = Column(String(15), nullable=False, unique=True)
    date_created = Column(DateTime, default = datetime.now)
    owner_id = Column(Integer, ForeignKey('user.user_id'))

    owner = relationship("User", back_populates="user_details", uselist=False)

class User_description(Base):
    __tablename__ = 'user_description'
    user_description_id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey('user.user_id'))

    owner = relationship('User', back_populates='user_description', uselist=False)

class Store_match(Base):
    __tablename__ = 'store_matches'
    matches_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phone_number = Column(String(15), unique=True)
    min_age = Column(Integer)
    max_age  = Column(Integer)
    county = Column(String(250))
    gender = Column(String(10))
    remaining_matches = Column(String(200))
    
class Process_Yes(Base):
    __tablename__ = 'process_yes'
    yes_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    requester_phone_number = Column(String(15), unique=True)
    requester_name = Column(String(50))
    notified_phone_number = Column(String(50), unique=True)
        
    
class Messages(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    message = Column(String(600))
    From = Column(String(15), nullable=False)
    To = Column(String(255))
    date_message_sent = Column(DateTime, default=datetime.now)
   
   