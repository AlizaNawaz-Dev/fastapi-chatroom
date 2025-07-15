from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends,status
from ..core.connection_manager import ConnectionManager
from .. import models
from sqlalchemy.orm import Session
from  ..core.databases import get_db
from ..core.oauth2_socket import get_user_from_token


router=APIRouter(prefix='/ws/chat',
                 tags=["Real-Time Chatting"])
manager=ConnectionManager()

@router.websocket('/{room_id}')
async def wsendpoint(room_id:int,websocket:WebSocket,db: Session = Depends(get_db)
):
      room=db.query(models.Chatroom).filter(models.Chatroom.room_id==room_id).first()
      if not room:
        await websocket.accept()
        await websocket.send_json({"error": f"There is no room with Id: {room_id} "})
        await websocket.close()
        return
      
      auth_header = websocket.headers.get("authorization")
      if not auth_header or not auth_header.startswith("Bearer "):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
      token = auth_header.split(" ")[1]
      current_user = get_user_from_token(token, db)

      await manager.connect(room_id,websocket)
      try:
        while True:
                
                data= await websocket.receive_text()
                new_msg=models.Message(content=data,home_id=room_id,owner=current_user.user_id,room_name=room.room_name)
                db.add(new_msg)
                db.commit()
                db.refresh(new_msg)
                await manager.broadcast(room_id,f"{current_user.username}: {data}")
      except WebSocketDisconnect:
        await manager.disconnect(room_id,websocket)
        await manager.broadcast(room_id,f"A User Left The Chat")
        await websocket.close()
      

       


