from tkinter import CASCADE
from .core.databases import Base
from sqlalchemy import Column, ForeignKey,Integer,String,TIMESTAMP,text,Boolean
from sqlalchemy.orm import relationship


class Chatroom(Base):
    __tablename__="chatrooms"

    room_id=Column(Integer,primary_key=True,nullable=False)
    room_name=Column(String(300),nullable=False)
    is_private=Column(Boolean,default=False) 
    #Which user created any room
    admin_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)

    room_admin=relationship("User")               
    room_msgs=relationship("Message")           
    

class User(Base):
    __tablename__="users"

    user_id=Column(Integer,primary_key=True,nullable=False)
    username=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=False)
    

class Message(Base):
    __tablename__="messages"

    msg_id=Column(Integer,nullable=False,primary_key=True)
    content=Column(String(1000),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=False)
    owner=Column(Integer,nullable=False)
    
    #This message will go to which room
    home_id=Column(Integer,ForeignKey("chatrooms.room_id",ondelete="CASCADE"),nullable=False)
    room_name=Column(String(255),server_default='Stovis Chatroom')
    
