from fastapi import FastAPI
from routers import websocket as websocket_router 

app = FastAPI()

app.include_router(websocket_router)

