from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime

#Schemas for Getting response
#schema for sending messages
class Send_msg(BaseModel):
    #user_id:int
    content:str=Field(..., min_length=1, max_length=250)
    room_name:Optional[str]="Stovis Chatroom"

#schema for user registration
class Register_user(BaseModel):
     username:str#= Field(..., min_length=3, max_length=30,pattern=r"^[a-zA-Z0-9_-]+$",
                  #       description="Only letters, numbers, underscores, and dashes allowed")
     email:EmailStr
     password:str= Field(..., min_length=8, max_length=100)

#schema for token data
class Tokendata(BaseModel):
    user_id:int
     
#schema for creating chatroom
class create_room(BaseModel):
    room_name:str#=Field(...,pattern=r"^[a-zA-Z_-]+$",
                  #       description="Only letters, underscores, and dashes allowed")
    is_private:Optional[bool]

#schema for user login
class Login_user(BaseModel):
     email:EmailStr
     password:str

#Schema for Room Deletion
class Delete_room(BaseModel):
    room_name:str

#schemas for sending back response
#schema for getting back messages
class Get_msg(BaseModel):
    room_name:str
    msg_id:int
    content:str
    created_at:datetime
    owner:int

    class Config:
        from_attributes = True

#For sending users information
class User_info(BaseModel):
    user_id:int
    username:str

    class Config:
        from_attributes = True

#schema for getting back chatrooms
class Get_rooms(BaseModel):
    room_name:str
    is_private:bool
    room_admin:User_info

    class Config:
        from_attributes = True
        
#schema for sending back messages
class send_room_msgs(BaseModel):
    content:str
    class Config:
        from_attributes = True
