from fastapi import WebSocket, WebSocketDisconnect
from storage.in_memory_store import game_sessions
import json

# Active WebSocket connections per game
# {
#   "game_id": [websocket1, websocket2]
# }

active_connections: dict[str, list[WebSocket]] = {}


# WebSocket endpoint handler
async def quiz_websocket(
    websocket: WebSocket,
    game_id: str,
    player_name: str
):
    await websocket.accept()

    # Validate game
    game = game_sessions.get(game_id)
    if not game:
        await websocket.send_text(json.dumps({
            "type": "ERROR",
            "payload": {"message": "Invalid game ID"}
        }))
        await websocket.close()
        return

    # Register connection
    active_connections.setdefault(game_id, []).append(websocket)

    # Notify other players
    await broadcast_event(
        game_id,
        "PLAYER_CONNECTED",
        {"player": player_name}
    )

    try:
        # Keep connection alive
        while True:
            # We don't process messages from client
            await websocket.receive_text()

    except WebSocketDisconnect:
        # Remove socket
        active_connections[game_id].remove(websocket)

        await broadcast_event(
            game_id,
            "PLAYER_DISCONNECTED",
            {"player": player_name}
        )


# Broadcast structured events
async def broadcast_event(
    game_id: str,
    event_type: str,
    payload: dict | None = None
):
    connections = active_connections.get(game_id, [])

    if not connections:
        return

    message = {
        "type": event_type,
        "payload": payload or {}
    }

    dead_connections = []

    for ws in connections:
        try:
            await ws.send_text(json.dumps(message))
        except Exception:
            dead_connections.append(ws)

    # Cleanup dead sockets
    for ws in dead_connections:
        connections.remove(ws)
