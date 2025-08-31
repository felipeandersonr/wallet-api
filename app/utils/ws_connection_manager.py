from loguru import logger
from fastapi import WebSocket


class ConnectionManager: 
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()

        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected via WebSocket.")


    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        logger.info(f"User {user_id} disconnected from WebSocket.")
    

    async def send_personal_message(self, user_id: int, message: dict):
        if user_id in self.active_connections.keys(): 
            websocket = self.active_connections[user_id]
            
            await websocket.send_json(message)
            logger.info(f"Sent message to user {user_id} via WebSocket.")
    

    async def send_message_to_broadcast(self, message: dict):
        for websocket in self.active_connections.values():
            await websocket.send_json(message)
            logger.info("Sent broadcast message to all connected WebSocket clients.")


ws_connection_manager = ConnectionManager()
