from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils import ws_connection_manager


router = APIRouter()
manager = ws_connection_manager


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
        
    except WebSocketDisconnect:
        manager.disconnect(user_id)
