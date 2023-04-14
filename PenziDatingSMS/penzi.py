from fastapi import FastAPI, Depends
import schemas

from functions import check_user_registration, process_start, process_details, process_description, process_match,\
    process_requested_details, process_requested_description, process_next_match, send_request_to_the_other_person
from pydantic import BaseModel
import json
import requests
from fastapi.middleware.cors import CORSMiddleware
from functions import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from performCRUD import save_sent_messages
app = FastAPI()

# Configure middleware to avoid the CORS error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class Item(BaseModel):
    phone_number: str
    message: str

class WaMsg(BaseModel):
    ack: int
    from_: str
    body: str
    
    class Config:
        fields = {
            'from_':'from'
        }
    
# Handle all the functionality
def main_engine(phone_number, message,  db: Session = next(get_db())):
    message_sent = {
            'From':phone_number,
            'message':message,
            'To':'Onfon',
            'date_message_sent':datetime.now(),
            
        }
    save_sent_messages(db, received_message=message_sent,)
    
    if message.startswith('254'):
        return_message = 'To get started send the word PENZI'
        return return_message

    if message.upper() == 'PENZI':
       user_registration = check_user_registration(phone_number)
       message_sent = {
            'From':'Onfon',
            'message':user_registration,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
       save_sent_messages(db, received_message=message_sent,)
       return user_registration
    
    elif message.upper().startswith('START'):
        start_response = process_start(phone_number,message)
        message_sent = {
            'From':'Onfon',
            'message':start_response,
            'To':phone_number,
            'date_message_sent':datetime.now(),
            
        }
        save_sent_messages(db, received_message=message_sent,)
       
        return start_response
    elif message.startswith('details'):
        response2 = process_details(phone_number, message,user_details=schemas.User_details)
        message_sent = {
            'From':'Onfon',
            'message':response2,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,) 
        return response2
    elif message.upper().startswith('MYSELF'):
         description_response = process_description(phone_number, message)
         message_sent = {
            'From':'Onfon',
            'message':description_response,
            'To':phone_number,
            'date_message_sent':datetime.now()
            }
         save_sent_messages(db, received_message=message_sent,) 
         return  description_response
    elif message.upper().startswith('MATCH'):
        match_response = process_match(phone_number, message)
        message_sent = {
            'From':'Onfon',
            'message':match_response,
            'To':phone_number,
            'date_message_sent':datetime.now()
            }
        save_sent_messages(db, received_message=message_sent,)
        return match_response 
    elif message.upper() == 'NEXT':
        next_matches = process_next_match(phone_number)
        message_sent = {
            'From':'Onfon',
            'message':next_matches,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,)
        return next_matches
    elif message.startswith('07'):
        requested_details =  process_requested_details(phone_number,message)
        message_sent = {
            'From':'Onfon',
            'message':requested_details,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,)
        return requested_details
    elif message.upper().startswith('DESCRIBE'):
        requested_description = process_requested_description(phone_number, message)
        message_sent = {
            'From':'Onfon',
            'message':requested_description,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,)
        return requested_description
    elif message.upper() == 'YES':
        requested_details_by_yes = send_request_to_the_other_person(phone_number)
        message_sent = {
            'From':'Onfon',
            'message':requested_details_by_yes,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,)
        return requested_details_by_yes
        
    else:
        return_invalid =  'invalid request'
        message_sent = {
            'From':'Onfon',
            'message':return_invalid,
            'To':phone_number,
            'date_message_sent':datetime.now()
        }
        save_sent_messages(db, received_message=message_sent,)
        return return_invalid
    
    
def whatsapp_api_test(phone_number, message: str):
    url = "https://wa.e-notice.co.ke/api/v1/messages/"
    payload = json.dumps({
            "receiver": phone_number,
            "text": message
        })
    headers = {
            
            'Authorization': 'Bearer b4560972fc5a256a437aca1e3c861a1c1b93dccc',
            'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)    
    print(f"http resonse: {response.status_code} -> {response.text}")

@app.post("/penzi")
def start(body: Item):
    
        # phone_number = body.from_.replace('@c.us', '')
        # message = body.body
        phone_number = body.phone_number
        message = body.message
        response = main_engine(phone_number=phone_number, message=message)
        print(f"response: {response}" )
        # whatsapp_api_test(phone_number=phone_number, message=response)        
        return {"reply": response, "status": 0}
    # except:
    #     return{"reply": "Error", "status": 1}
       
  
# print(main_engine('254748804536', "PENZI")) 
# print(main_engine('254711113333', "start#Kevin Lucky#25#Male#Nairobi#Karen"))
# print(main_engine('254748804536', "details#graduate#Aeronautical Engineer#single#christian#Bukusu")) 
# print(main_engine('254744443333', "MYSELF Cute,loving, caring "))
# print(main_engine('254711113444', 'match#18-40#nairobi'))
# print(main_engine('254711113444', "next"))  
# print(main_engine('254748804536', '0712335000'))  
# print(main_engine('254748804536', 'DESCRIBE 0795123265'))
# print(main_engine('254771324545', 'next'))
# print(main_engine('254777544532', 'YES'))  


       
