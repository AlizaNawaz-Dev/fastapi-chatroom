from fastapi import APIRouter,Depends,status,HTTPException,Path
from .. import schemas,models
from ..core.databases import get_db
from sqlalchemy.orm import Session
from ..core import oauth2
from typing import List,Optional
import regex as re
router=APIRouter(prefix='/api/chat/rooms',
                 tags=["ChatRooms"])

#Creating chatrooms
@router.post('/create')
def create_room(data:schemas.create_room,db: Session=Depends(get_db),current_user: int= Depends(oauth2.Get_Current_User)):
   # user_data=db.query(models.User).filter(models.User.user_id==current_user.user_id)
    room=models.Chatroom(**data.model_dump(),admin_id=current_user.user_id)
    name=db.query(models.Chatroom).filter(models.Chatroom.room_name==data.room_name).first()
    if name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Chatroom with this name already exsists. ")
    db.add(room)
    db.commit()
    db.refresh(room)          
    return room
    
#Get all chatrooms
@router.get('/',response_model=List[schemas.Get_rooms])
def get_all(db: Session=Depends(get_db),current_user: int= Depends(oauth2.Get_Current_User),limit:int=10,search:Optional[str]=""):
    data=db.query(models.Chatroom).outerjoin(models.User).filter(models.Chatroom.admin_id==models.User.user_id).filter(models.Chatroom.room_name.contains(search)).limit(limit).all()
    return data

#Get Specific Chatroom and it's creator
@router.get('/{id}',response_model=schemas.Get_rooms)
def get_chatroom(id:int,db: Session=Depends(get_db),current_user: int= Depends(oauth2.Get_Current_User)):

    room=db.query(models.Chatroom).filter(models.Chatroom.room_id==id)
    if room.first():
        data=room.outerjoin(models.User).filter(models.Chatroom.admin_id==models.User.user_id).first()
        return data
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Room with this id don't exists. ")

#Delete chatroom
@router.delete('/{name}')
def delete_room(name:str=Path(...),db: Session=Depends(get_db),current_user: int= Depends(oauth2.Get_Current_User)):
   # pattern = r"^[a-zA-Z_-]+$"
    # if not re.match(pattern, name):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Invalid room name. Only letters, spaces, underscores (_) and dashes (-) are allowed."
    #     )
    room=db.query(models.Chatroom).filter(models.Chatroom.room_name==name)
    data=room.first()
    if data:
      if data.admin_id==current_user.user_id:
        room.delete(synchronize_session=False)
        db.commit()
        return "Room Deleted Successfully"
      else:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admins can delete room")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No chatroom with this name")



