from fastapi import WebSocket
from typing import List,Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections:Dict[int,List[WebSocket]] = {}

    #Establish connection
    async def connect(self,room_id:int,websocket:WebSocket):
        await websocket.accept()                                   #Handshake
        if room_id not in self.active_connections:
            self.active_connections[room_id]=[]

        self.active_connections[room_id].append(websocket)

    #Disconnect connection
    async def disconnect(self,room_id:int,websocket:WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    #Sending message to active user like welcome msg
    async def send_personal_msg(self,message:str,websocket:WebSocket):
        await websocket.send_text(message)

    #Broadcasting sending msg to all active users
    async def broadcast(self,room_id:int,message:str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
               await connection.send_text(message)






    