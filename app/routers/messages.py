from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from ..core import databases,oauth2
from .. import schemas,models
from typing import Optional,List
from sqlalchemy.orm import Session


router=APIRouter(prefix='/api/chat/msgs',
                 tags=["Messages"])

#Add message to specific chatroom
@router.post('/',response_model=schemas.Get_msg)
def add_msg(msgs:schemas.Send_msg,db: Session=Depends(databases.get_db),current_user=Depends(oauth2.Get_Current_User)):

    room=db.query(models.Chatroom).filter(models.Chatroom.room_name==msgs.room_name).first()
    if room:
        room_id=room.room_id
        msg=models.Message(**msgs.model_dump(),owner=current_user.user_id,home_id=room_id)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No chatroom with this name :()")

#Retreive messages from specific chatroom
@router.get('/{id}',response_model=List[schemas.send_room_msgs])
def get_msg_from_chatroom(id:int,db: Session=Depends(databases.get_db),current_user: int= Depends(oauth2.Get_Current_User),search:Optional[str]="",limit: int = 10,
    offset: int = 0):
    data=db.query(models.Chatroom).filter(models.Chatroom.room_id==id).first()
    if data:
      msg_query=db.query(models.Message).filter(models.Message.home_id==id)
      if data.is_private:
        participated = any(msg.owner == current_user.user_id for msg in msg_query)
        if not participated:
                raise HTTPException(status_code=403, detail="You are not a participant of this room")
      msgs = msg_query.filter(models.Message.content.contains(search)).order_by(models.Message.created_at.desc()).offset(offset).limit(limit).all()
      if not msgs:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=("No messages found for this room"))
      return msgs      
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No chatroom found with id: {id}")

#Getting messages by specific user
@router.get('/{user_id}/user',response_model=List[schemas.send_room_msgs])
def get_user_messages(user_id:int,db: Session=Depends(databases.get_db)):
    user=db.query(models.User).filter(models.User.user_id==user_id).first()
    if user:
        msgs=db.query(models.Message).filter(models.Message.owner==user_id).all()
        if msgs:
            return msgs
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No messages found for id: {user_id}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No User exist with id: {user_id}")

#Deleting messages
@router.delete('/{id}')
def delete_msg(id :int,db: Session=Depends(databases.get_db),current_user: int= Depends(oauth2.Get_Current_User)):
    msg_query=db.query(models.Message).filter(models.Message.msg_id==id)
    msg=msg_query.first()
    if msg:
        if msg.owner==current_user.user_id:
            content=msg.content
            msg_query.delete(synchronize_session=False)
            db.commit()
            return f"Message:{content}   Deleted Successfully"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only Sender can delete this message")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Message not found!")






