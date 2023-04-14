from fastapi import FastAPI, Depends, HTTPException
from typing import Union, Dict, List
import models, schemas
from db_config import db_engine, SessionLocal
from sqlalchemy.orm import Session
import itertools 
from sqlalchemy import and_
from datetime import datetime
# creating database tables


# @app.get("/ap1/users", response_model=List[schemas.User])
# def read_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     for i in users:
#         return i


# @app.post("/ap1/users", response_model=schemas.User)
# def register_user(user:schemas.User, db: Session = Depends(get_db)):
#     db_user = models.User(**user.dict())
#     db.add(db_user)
#     db.commit()
#     print(type(db_user))
#     return db_user 


# @app.post("/ap2/userDetails", response_model=schemas.User_details )
# def post_user_detail(user_details:schemas.User_details, db:Session = Depends(get_db)):
#     db_user_details = models.User_details(**user_details.dict())
#     db.add(db_user_details)
#     db.commit()
#     return db_user_details 


# @app.get("/ap2/userDetails", response_model=List[schemas.User_details])
# def read_users(db: Session = Depends(get_db)):
#     users_details = db.query(models.User_details).all()
#     return users_details

# @app.post("/ap2/userDescription", response_model=schemas.User_description )
# def post_user_detail(user_description:schemas.User_description, db:Session = Depends(get_db)):
#     db_user_description = models.User_description(**user_description.dict())
#     db.add(db_user_description)
#     db.commit()
#     return db_user_description     

# @app.get("/ap2/userDescription", response_model=List[schemas.User_description])
# def read_users(db: Session = Depends(get_db)):
#     users_description = db.query(models.User_description).all()
#     return users_description

# >>>>>>>>>>>>>>>>>>>>>>>>>>> Create >>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
def read_registered_users(db:Session):
    phone_number = []
    users = list(db.query(models.User.phone_number).all())
   
    for i in users:
        phone_number.append
        for p in i:
            phone_number.append(p)
    return(phone_number)
    
   
  
def add_user_to_db(user:schemas.User,db:Session):
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(type(db_user))
    return db_user 

def create_user_details(db:Session, user_details:schemas.User_detailsCreate, user_id:int):
    db_user_details = models.User_details(**user_details, owner_id = user_id)
    db.add(db_user_details)
    db.commit()
    db.refresh(db_user_details)
    return db_user_details 

def create_user_description(db:Session, user_description:schemas.User_descriptionCreate, user_id:int):
    db_user_description = models.User_description(description = user_description, owner_id = user_id)
    db.add(db_user_description)
    db.commit()
    db.refresh(db_user_description)
    return db_user_description

def save_remaining_matches(db:Session, remaining_matches: schemas.Store_matchCreate,):
    db_save_remaining_matches = models.Store_match(**remaining_matches)
    db.add(db_save_remaining_matches)
    db.commit()
    db.refresh(db_save_remaining_matches)
    
def update_remaining_matches(db:Session, remaining_matches_IDs: str, phone_number:str):
    all_matches_remaining = db.query(models.Store_match).filter(models.Store_match.phone_number == phone_number).first()
    if not  all_matches_remaining:
        return 'at the moment there are no additional matches available'
    all_matches_remaining.remaining_matches = remaining_matches_IDs
    db.commit() 
    db.refresh(all_matches_remaining)  
    return all_matches_remaining

def save_yes_details(db:Session, yes_details: schemas.Process_yesCreate):
    db_save_yes_details = models.Process_Yes(**yes_details)
    db.add(db_save_yes_details)
    db.commit()
    db.refresh(db_save_yes_details)
# >>>>>>>>>>>>>>>>>>>>>>>>>>> READ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #

def get_users_by_age_and_county(db: Session,  county: str, start_age: int, last_age:int, gender: str):
    users_of_that_ageCounty = db.query(models.User).filter(and_(models.User.age <= last_age, models.User.age >= start_age),
                                                           models.User.county == county, models.User.gender == gender).all()
    return users_of_that_ageCounty

def get_gender(db: Session, phone_number: str):
    gender = []
    user_gender = db.query(models.User.gender).filter(models.User.phone_number == phone_number).all()
    for i in user_gender:
        for genderall in i:
            gender.append(genderall)
    return gender


def read_details_of_requested_user(db:Session, phone_number:str) :
    userS_details = db.query(models.User, models.User_details).join(models.User).filter(models.User.phone_number == phone_number).all()
    return userS_details


def read_id(db:Session, phone_number: str):
    id = []
    user_id = db.query(models.User.user_id).filter(models.User.phone_number == phone_number).all()
    for i in user_id:
        for id2 in i:
            id.append(id2)
    return id   

def read_description_requested_by_user(db:Session, phone_number:str):
    user_description = db.query(models.User, models.User_description).join(models.User).filter(models.User.phone_number == phone_number).all()
    return user_description

def read_three_users(db:Session,county: str, start_age: int, last_age:int, gender:str, offset:int ):
    three_user_details = db.query(models.User.name, models.User.age, models.User.phone_number).filter(and_(models.User.age <= last_age, models.User.age >= start_age),
                                                           models.User.county == county, models.User.gender == gender).offset(offset).limit(3).all()
    return three_user_details
    
def read_next_three_users(db:Session,county: str, start_age: int, last_age:int, gender:str ):
    next_three_user_details = db.query(models.User.name, models.User.age, models.User.phone_number).filter(and_(models.User.age <= last_age, models.User.age >= start_age),
                                                           models.User.county == county, models.User.gender == gender).offset(3).limit(3).all()
    return next_three_user_details
          
def read_ids_of_the_next_matches(db:Session, phone_number: str):
    next_three_matches = db.query(models.Store_match).filter(models.Store_match.phone_number == phone_number).first()
    return next_three_matches

def read_the_next_matches(db:Session, remaining_IDs: int):
    next_matches = db.query(models.User).filter(models.User.user_id.in_(remaining_IDs)).all()
    return next_matches

def get_user_info_by_phone_number(db:Session, phone_number: str):
    user_info = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    return user_info

def get_phone_number_from_yes_table(db:Session, phone_number: str):
    requester_phone_number = db.query(models.Process_Yes.requester_phone_number).filter(models.Process_Yes.notified_phone_number == phone_number).first()
    if not requester_phone_number:
        return " not acceptable !!!!!"
    else:
        for phone in requester_phone_number:
            return phone

#............. save messages ...................#
def get_user_names(db:Session, phone_number:str):
    name = db.query(models.User.name).filter(models.User.phone_number == phone_number).first()
    # for nam in name:
    return name
def save_sent_messages(db:Session, received_message: schemas.MessageCreate):
    db_received_messages = models.Messages(**received_message)
    db.add(db_received_messages)
    db.commit()
    db.refresh(db_received_messages)
    db.rollback()
    
def add_sent_messages_by_update(db:Session, sent_message: str, time_sent: datetime,phone_number: str, message: str):
    user_in_message_received = db.query(models.Messages).filter(and_(models.Messages.message_received == 'NEXT', models.Messages.phone_number == phone_number))
        

# >>>>>>>>>>>>>>>>>>>>>> DELETE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
def delete_store_match(db: Session, store_match: models.Store_match):
    # detaching the object from the previous session 
    db_exp = db.object_session(store_match)
    db_exp.expunge(store_match)
    db.delete(store_match)
    db.commit()
    
def delete_process_yes(db:Session, phone_number: str):
     process_yes = db.query(models.Process_Yes).filter(models.Process_Yes.requester_phone_number==phone_number).first()
     if process_yes:
         db.delete(process_yes)
         db.commit()

    