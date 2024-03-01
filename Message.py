import requests


class Message:
    def __init__(self, data, cache, header):
        self.header = header

        self.files = []
        self.buttons = []
        self.mentions = []
        self.quote = []

        self.channel_numeric_id = None
        self.creator = None

        self.message_numeric_id = None
        self.created = None

        self.syncMessage(data, cache)

    def __repr__(self):
        return f"{self.__class__.__name__}<messageId : {self.message_numeric_id}, channelId : {self.channel_numeric_id}, creator : {self.creator}>"

    def syncMessage(self, data, cache):
        self.channel_numeric_id = data["channelId"]

        # For some reason the D is capitalised here... ??
        self.message_numeric_id = data["messageID"]
        self.created = data["created"]

        self.creator = (cache["user_cache"]).get(data["creator"]["id"])

        self.files = data.get("files", [])
        self.buttons = data.get("buttons", [])
        self.mentions = data.get("mentions", [])

        channel = None
        for server in (cache["server_cache"]).values():
            if server.get_channel(self.channel_numeric_id) is not None:
                channel = server.get_channel(self.channel_numeric_id)

        if channel is None:
            raise TypeError("Received a message for an unknown (uncached) channel !")  # TODO: Replace with custom error

        self.quote = [channel.getMessage(messageId) for messageId in data.get("quotes")
                      if channel.getMessage(messageId) is not None]


class TextMessage(Message):
    def __init__(self, data, cache, header):
        super().__init__(data, cache, header)

        self.content = None

        self.syncTextMessage(data)

    def syncTextMessage(self, data):
        self.content = data.get("message", "")

    async def delete(self):
        # TODO: Implement some class that handles all requests & error handling
        response = requests.delete(f"https://nertivia.net/api/messages/{self.message_numeric_id}/channels/{self.channel_numeric_id}", headers=self.header)

        return response

class WelcomeMessage(Message):
    pass
