from simple_print import sprint
from channel_box import ChannelBoxEndpoint


class ChatChannel(ChannelBoxEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expires = 16000
        self.encoding = "json"

    async def on_connect(self, websocket):
        sprint('ChatChannel -> on_connect', c="green")
        channel_name = websocket.query_params.get("channel_name", "LordaeronChat") 
        await self.channel_get_or_create(channel_name, websocket) 
        await websocket.accept()

    async def on_receive(self, websocket, data):
        sprint(f'ChatChannel -> on_recive {data}', c="green")
        author = data["author"] 
        text = data["text"]    
        avatar = data.get("avatar", "5")        
        if message.strip():
            payload = {
                "author": author,
                "text": text,
                "avatar": avatar 
            }
            await self.channel_send(payload)