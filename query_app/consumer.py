from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from .tasks import * 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class FetchComsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("ws connected")
        await self.channel_layer.group_add('fetch_data', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("ws disconnted")
        await self.channel_layer.group_discard('fetch_data', self.channel_name)

    async def receive(self, text_data):
        print("inside receiver")
        data_json = json.loads(text_data)
        id = data_json['message']
        print("id in consumer ", id , type(id))
        
        data_fetch.delay(id)
        print("ended receiver")

    async def task_message(self, event):
        print("inside task_message")
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))