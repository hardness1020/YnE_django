import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    # Called when a new WebSocket connection is established
    async def connect(self):
        await self.accept()
        
    # Called when a WebSocket connection is closed
    async def disconnect(self, close_code):
        pass
    
    # Called when a WebSocket recieved a message
    # TODO: This function is now simply echos back the received message to the client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
