from pydantic import BaseModel
import datetime
from typing import List


class User_detailsBase(BaseModel):
    level_of_education:str
    profession:str
    marital_status:str
    religion:str
    ethnicity:str
    date_created: datetime.datetime

class User_detailsCreate(User_detailsBase):
    pass

class User_details(User_detailsBase):
    id:int
    owner_id : int

    class Config:
        orm_mod = True

class User_descriptionBase(BaseModel):
    description:str

class User_descriptionCreate(User_descriptionBase):
    pass

class User_description(User_descriptionBase):
    user_description_id:int
    owner_id:int

    class Config:
        orm_mode = True

class MessagesBase(BaseModel):
    message:str
    date_message_sent:datetime.datetime
    From:str
    To:str
          

class MessageCreate(MessagesBase):
    pass

class Messages(MessagesBase):
    message_id: int
    
    class Config:
        orm_mode = True
class UserBase(BaseModel):
    name:str
    age:int
    gender:str
    county:str
    town:str
    phone_number:str
    date_registered:datetime.datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    id:int
    is_active: bool
    user_details:List[User_details] = []
    user_description:List[User_description] = []
    class Config:
        orm_mode = True



# Messages = []    

class Store_matchBase(BaseModel):
    phone_number: str
    county: str
    min_age: int
    max_age: int
    gender: str
    remaining_matches: str
    
class Store_matchCreate(Store_matchBase):
    pass

class Store_match(Store_matchBase):
    matches_id: int  
    
    class Config:
        orm_mod = True  
        
class Process_yesBase(BaseModel):
    requester_phone_number: str
    requester_name: str
    notified_phone_number: str
    
class Process_yesCreate(Process_yesBase):
    pass 

class Process_yes(Process_yesBase):
    yes_id : int
    
    class Config:
        orm_mode = True           