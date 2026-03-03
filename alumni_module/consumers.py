import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conv_id = self.scope["url_route"]["kwargs"]["conv_id"]
        self.room_group_name = f"call_{self.conv_id}"

        # optional: only authenticated users
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Pass signaling messages between users:
        - offer
        - answer
        - ice
        - hangup
        """
        data = json.loads(text_data)
        data["sender"] = self.scope["user"].username

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "signal_message", "message": data}
        )

    async def signal_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))