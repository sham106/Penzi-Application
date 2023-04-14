from performCRUD import read_registered_users, add_user_to_db, Session, get_gender, get_users_by_age_and_county, create_user_details,\
      read_details_of_requested_user, read_id, create_user_description, read_description_requested_by_user, read_three_users,\
          read_next_three_users, save_remaining_matches, read_ids_of_the_next_matches, read_the_next_matches, update_remaining_matches,\
              delete_store_match, get_user_info_by_phone_number, save_yes_details, get_phone_number_from_yes_table, get_user_names, save_sent_messages,\
                  delete_process_yes
from fastapi import FastAPI, Depends
import schemas, models
import performCRUD
from k_counties.kenya import get_counties
from sqlalchemy.orm import Session
from db_config import db_engine, SessionLocal
from datetime import datetime
import time
import requests
import json

models.Base.metadata.create_all(bind=db_engine)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

kenyan_counties = get_counties()
kenyan_counties_only = [item.split()[0] for item in kenyan_counties]




def check_user_registration(phone_number, db: Session = next(get_db())):
    name = get_user_names(db, phone_number=phone_number)
    user_id = read_id(next(get_db()), phone_number=phone_number)
    phone_numbers = read_registered_users(next(get_db()))
    if phone_number in phone_numbers:   
        return_message = "You were registered for dating with your initial details.To search for a MPENZI, SMS match'#'age'#'town to 22141 and meet the person of your dreams.E.g., match'#'23-25'#'Nairobi "
        return return_message
    else:
        return2_message = "Welcome to our dating service with 6000 potential dating partners!To register SMS start'#name'#'age'#'gender'#'county'#'town to 22141.E.g., start'#John Doe#26#Male#Nakuru#Naivasha"
        return return2_message


# ...........Using next because Depends mainly works on FastAPI routes..........

def process_start(phone_number,message, db: Session = next(get_db())):
    items = message.split('#')
    if len(items) != 6:
        return 'you have not entered all the details'
    name = items[1].split(' ')
    if len(name) < 1:
        return 'name is not correct'
    if not items[2].isnumeric(): #and int(items[2]) < 18:
        return 'age is invalid!'
    if int(items[2]) < 18:
        return 'you are under age'
    if items[3].lower() != 'male' and items[3].lower() != 'female':
        return 'gender is not correct'
    if items[4].capitalize() not in kenyan_counties_only:
        return 'county is not correct'
    else:
        user = dict(
            name = items[1],
            age = items[2],
            gender = items[3],
            county = items[4],
            town = items[5],
            phone_number = phone_number
        )

        add_user_to_db(db = db, user=user)
        fast_name = name[0]
        return_message2 = f'Your profile has been created successfully {fast_name}.SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.E.g. details#diploma#driver#single#christian#mijikenda'
        return return_message2


def process_details(phone_number: str, message: str, user_details:schemas.User_detailsCreate, db : Session = next(get_db())):
    items = message.split('#')
    name = get_user_names(db, phone_number=phone_number)
    user_id = read_id(next(get_db()), phone_number=phone_number)

    if len(items) != 6 :   
        return_message3 = 'you have not entered all the detais'
        return return_message3
    
    else:
        user_details = dict(
            level_of_education = items[1],
            profession = items[2],
            marital_status = items[3],
            religion = items[4],
            ethnicity = items[5],
            phone_number = phone_number,

        )
        user_id = read_id(next(get_db()), phone_number=phone_number)
        for id in user_id:           
            create_user_details(db = db, user_details=user_details, user_id=id)
        return_message33 = "This is the last stage of registration.SMS a brief description of yourself to 22141 starting with the word MYSELF.E.g., MYSELF chocolate, lovely, sexy etc." 
        return return_message33


def process_description(phone_number, message, db : Session = next(get_db())):
    items = message.split(',')
    name = get_user_names(db, phone_number=phone_number)
    user_id = read_id(next(get_db()), phone_number=phone_number)
    if len(items) < 3:
        return_message4 = 'You have entered very few description,Please add more.'
        return return_message4
    else:

        user_description = message.upper().split(' ')
        user_description.remove('MYSELF')
        string_user_description = ' '.join(user_description)
    
        user_id = read_id(next(get_db()), phone_number=phone_number)
        for id in user_id:
            create_user_description(db=db, user_description=string_user_description, user_id=id)
        # Save message 
        return_message44 = 'You are now registered for dating.To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams.E.g., match#23-25#Kisumu'      
        return return_message44
    
def process_match(phone_number, message,  db : Session = next(get_db())):      
    items = message.split("#")
    name = get_user_names(db, phone_number=phone_number)
    user_id = read_id(next(get_db()), phone_number=phone_number)
    
    if len(items) != 3 :
        return 'you have not entered all the search details'  
                        
    age_range = items[1].split('-')
    if len(age_range) !=2 :
        return 'age range not correct'
    elif int(age_range[0]) < 18:
        return 'age cannot be below 18'
    elif int(age_range[0]) > int(age_range[1]):
        return 'start age cannot be larger than end age!!!'
    elif items[2].capitalize() not in kenyan_counties_only:
        return'That is not a Kenyan County'
    else:
        start_age,last_age = items[1].split('-')
        start_age = int(start_age)
        last_age = int(last_age) 
        county = items[2]
        
    all_genders = []
    gender = get_gender(next(get_db()), phone_number=phone_number)
    gender_of_user = ''.join(gender)
    
    if not  gender_of_user:
        return 'Sorry you did not register, send the word PENZI to get started'
        
    if gender_of_user.lower()  == 'male':
        gender1 = 'female'
        skip = 0
        limit = 3
        requested_users = get_users_by_age_and_county(next(get_db()),  county = county, start_age=start_age, last_age= last_age, gender= gender1)
        number_of_ladies = len(requested_users)
        for lady in requested_users:
            lady_details = f'{lady.name}, aged {lady.age}, {lady.phone_number}'
                            
        if number_of_ladies == 1:
            return_message5 = f'We have {number_of_ladies} lady who match your choice!  We will send you her details shortly.{lady_details} To get more details about her, SMS her number e.g., 0722010203 to 2214' 
              
            return return_message5
                    
        elif number_of_ladies >= 2 and number_of_ladies <= 3:
            time.sleep(4)
            matches = []  
            first_three_ladies = requested_users[:3]
            for ladies in first_three_ladies:
                ladies_details = f"{ladies.name}, aged {ladies.age}, {ladies.phone_number}"
                matches.append(ladies_details)
                
            # save the remaining matches
            
            remaining_matches = ','.join(str(lady.user_id) for lady in requested_users[3:])
            search_data = {'phone_number': phone_number, 
                            'min_age': start_age,
                            'max_age': last_age,
                            'county': county,
                            'gender': gender_of_user, 
                            'remaining_matches': remaining_matches}
            
            save_remaining_matches(db, remaining_matches=search_data)
                
            out_put = '\n'.join(matches)
            number_of_ladies_remaining = max(number_of_ladies - 3, 0)
            
            # Save message
            return_message55 = f'We have {number_of_ladies} ladies who match your choice! We will send you their details  shortly.\nTo get more details about a lady, SMS her number e.g., 0722010203 to 2214\n{out_put}'
            return return_message55 
        
        elif number_of_ladies > 3:
            time.sleep(4)
            matches = []  
            first_three_ladies = requested_users[:3]
            for ladies in first_three_ladies:
                ladies_details = f"{ladies.name}, aged {ladies.age}, {ladies.phone_number}"
                matches.append(ladies_details)
                
            # save the remaining matches
            
            remaining_matches = ','.join(str(lady.user_id) for lady in requested_users[3:])
            search_data = {'phone_number': phone_number, 
                            'min_age': start_age,
                            'max_age': last_age,
                            'county': county,
                            'gender': gender_of_user, 
                            'remaining_matches': remaining_matches}
            
            save_remaining_matches(db, remaining_matches=search_data)
                
            out_put = '\n'.join(matches)
            number_of_ladies_remaining = max(number_of_ladies - 3, 0)
            
            # Save message
            return_message55 = f'We have {number_of_ladies} ladies who match your choice! We will send you details of 3 of them shortly.\nTo get more details about a lady, SMS her number e.g., 0722010203 to 2214\n{out_put}\nSend NEXT to 22141 to receive details of the remaining {number_of_ladies_remaining} ladies'
            return return_message55
                        
                        
        else:
            return ' users are not available '                        
            
           
            
    elif gender_of_user.lower() == 'female':
        gender2 = 'male'
        requested_users = get_users_by_age_and_county(next(get_db()),  county = county, start_age=start_age, last_age= last_age, gender= gender2 )
        number_of_gents = len(requested_users)
        
        matches = [] 
         
        first_three_gents = requested_users[:3]
        for gents in first_three_gents:
                gents_details = f"{gents.name}, aged {gents.age}, {gents.phone_number}"
                matches.append(gents_details)
             
        remaining_matches = ','.join(str(gent.user_id) for gent in requested_users[3:])
        search_data = {'phone_number': phone_number, 
                            'min_age': start_age,
                            'max_age': last_age,
                            'county': county,
                            'gender': gender_of_user, 
                            'remaining_matches': remaining_matches}
            
        save_remaining_matches(db, remaining_matches=search_data)  
            
        out_put = '\r\n'.join(matches)
        number_of_gents_remaining = max(number_of_gents - 3, 0)
        if number_of_gents == 1:
            return_message6 = f"We have {number_of_gents} gent who match your choice! We will send you his detals shortly.To get more details about him, SMS his number e.g., 0722010203 to 2214 >>>>> {out_put}"
           
            return return_message6
        elif number_of_gents >=2:
              
            return_message66 = f'We have {number_of_gents} gents who match your choice! We will send you details of 3 of them shortly.To get more details about a gent, SMS his number e.g., 0722010203 to 2214 >>>> {out_put}Send NEXT to 22141 to receive details of the remaining {number_of_gents_remaining} gents'   
            return return_message66
        
        else:
            return_message666 = 'sorry users of that age gap or county are not available now'
            return return_message666

def process_next_match(phone_number, db : Session = next(get_db())):
    all_matches_remaining = read_ids_of_the_next_matches(db, phone_number=phone_number)
    gender = get_gender(next(get_db()), phone_number=phone_number)
    gender_of_user = ''.join(gender)
    
    if not all_matches_remaining:
        return_message7 = 'Sory but you didnt initiate search before, send word PENZI to get started'
        return return_message7
    
    remaining_IDs = [int(id_str) for id_str in all_matches_remaining.remaining_matches.split(',') if id_str]
    matching_ladies = read_the_next_matches(db, remaining_IDs=remaining_IDs)
    
    matches = []  
    next_three_ladies = matching_ladies[:3]
    for ladies in next_three_ladies:
        ladies_details = f"{ladies.name}, aged {ladies.age}, {ladies.phone_number}"
        matches.append(ladies_details)
    
    remaining_matches_IDs = ','.join(str(lady.user_id) for lady in matching_ladies[3:])
    update_remaining_matches(db, phone_number = phone_number, remaining_matches_IDs=remaining_matches_IDs )
    
    if not remaining_matches_IDs:
        delete_store_match(db,store_match=all_matches_remaining )
    out_put = '\n'.join(matches)
    remaining_users = (len(matching_ladies) - 3)
    if remaining_users == 1 and  len(matching_ladies) > 1:
        if gender_of_user.lower() == 'male':
            return_message8 = f"{out_put} \nSend NEXT to 22141 to receive details of the remaining {remaining_users} lady"
            return return_message8
        else:
            return_message8 = f"{out_put} \nSend NEXT to 22141 to receive details of the remaining {remaining_users} gent"
            return return_message8
    elif remaining_users >= 1 and len(matching_ladies) > 1:
        if gender_of_user.lower() == 'male':
            return_message88 = f"{out_put} \nSend NEXT to 22141 to receive details of the remaining {remaining_users} ladies"
            return return_message88
        else:
            return_message88 = f"{out_put} \nSend NEXT to 22141 to receive details of the remaining {remaining_users} gents"
            return return_message88
    
    return_message9 = f"{out_put} This the END!!!"
    return return_message9

def process_requested_details(phone_number: str, message, db : Session = next(get_db())):
    remove_0 = message[1:]
    requested_phone_number = '254' + remove_0
    requested_details = read_details_of_requested_user(next(get_db()), phone_number = requested_phone_number)
    gender = get_gender(next(get_db()), phone_number=phone_number)
    gender_of_user = ''.join(gender)
    
    if not requested_details:
        return 'Sorry , the user has not send their details  '

    for user_and_details in requested_details:
        User = user_and_details[0]
        Details = user_and_details[1]
        name = User.name.split(' ')
        first_name = name[0]
        user_phone_number = User.phone_number
        remove_254 = user_phone_number[3:]
        phone_number_with_0 = '0' + remove_254    
    
    # Notify the other person
    user_info = get_user_info_by_phone_number(next(get_db()), phone_number=phone_number)
    
    # Save the detalis
    details = {
        "requester_phone_number": phone_number,
        "requester_name": user_info.name,
        "notified_phone_number": requested_phone_number
        
    }
    save_yes_details(next(get_db()), yes_details=details)
    
    return_message10 = f'{User.name} aged {User.age}, {User.county} County, {User.town} town,\n{Details.level_of_education}, {Details.profession}, {Details.marital_status},{Details.religion}, {Details.ethnicity}.\nSend DESCRIBE {phone_number_with_0} to get more details about {first_name}.'

    if gender_of_user.lower() == 'male':
    
        notification_message = f'\nHi {User.name} a man named {user_info.name} is interested in you and requested your details.He is aged {user_info.age} based in {user_info.county}.Do you want to know more about him? Send YES to 22141'
   
        return f'{return_message10} ,,,,,, {notification_message}'
    else:
        notification_message2 = f'\nHi {User.name} a lady named {user_info.name} is interested in you and requested your details.She is aged {user_info.age} based in {user_info.county}.Do you want to know more about her? Send YES to 22141'
        return f'{return_message10} ,,,,,, {notification_message2}'
   
              
def process_requested_description(phone_number, message, db:Session = next(get_db())):
    items = message.split(' ')
    requested_phone_number = items[1]
    remove_zero = requested_phone_number[1:]
    phone_number_with_code = '254' + remove_zero
    requested_description = read_description_requested_by_user(db, phone_number=phone_number_with_code)
    
    if not requested_description:
        return 'Sory the requested user has not send ther description'
    for specificDescription in requested_description:
        User = specificDescription[0]
        Description = specificDescription[1]
        user_name = User.name.split(' ')
        first_name = user_name[0]
        
        return_message11 = f'{first_name} DESCRIBES as {Description.description}'
        return return_message11

def send_request_to_the_other_person(phone_number, db:Session = next(get_db())):
    
    requester_phone_number = get_phone_number_from_yes_table(db, phone_number=phone_number)
    requested_details = read_details_of_requested_user(db, phone_number = requester_phone_number)
    if not requested_details:
        return_message12 = 'Sorry its either User was not send a notification or user has not yet send their details'
        return return_message12
    for details in requested_details:
        User = details[0]
        Details = details[1]
        
    first_name = User.name.split(" ")[0]
    user_phone_number = '0'+  User.phone_number[3:] 
    
    delete_process_yes(db, phone_number=requester_phone_number)

    return_message13 = f"{User.name} aged {User.age}, {User.county} County, {User.town} town, {Details.level_of_education}, {Details.profession}, {Details.marital_status}, {Details.religion}, {Details.ethnicity}.Send DESCRIBE {user_phone_number} to get more details about {first_name}."
       
    return return_message13

    