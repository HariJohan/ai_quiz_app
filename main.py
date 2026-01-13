from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.websocket import quiz_websocket

app = FastAPI(title="AI Quiz Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # for MVP (later restrict)
    allow_credentials=True,
    allow_methods=["*"],      # allows POST, GET, OPTIONS, etc
    allow_headers=["*"],
)


app.include_router(router)



@app.websocket("/ws/game/{game_id}/{player_name}")
# async def websocket_endpoint(websocket, game_id: str, player_name: str):
async def websocket_endpoint(
    websocket: WebSocket,   
    game_id: str,
    player_name: str
):
    await quiz_websocket(websocket, game_id, player_name)
