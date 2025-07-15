from fastapi import FastAPI
from .routers import users,chatroom,messages,chat_ws
from .core.databases import engine,Base
app=FastAPI(
    title="Chatroom API",
    description="A real-time chat backend with JWT, WebSockets, and MySQL")


#Base.metadata.create_all(engine)    #for db connectivity(if alembic is not in use)

app.include_router(users.router)
app.include_router(chatroom.router)
app.include_router(messages.router)
app.include_router(chat_ws.router)
