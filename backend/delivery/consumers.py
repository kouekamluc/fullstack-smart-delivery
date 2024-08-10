import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        latitude = text_data_json['latitude']
        longitude = text_data_json['longitude']

        # Send data back to WebSocket
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))
