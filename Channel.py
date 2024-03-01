import Permissions
import Message

class Channel:
    def __init__(self, data, header):
        self.alpha_numeric_id = None
        self.numeric_id = None
        self.type = None

        # Apparently categories have rate limits ? Huh
        self.rate_limit = None
        self.name = None

        self.alpha_numeric_server_id = None
        self.numeric_server_id = None

        self.icon = None

        self.permissions = None

        self.header = header

        self.syncChannel(data)

    def __eq__(self, other):
        # IDE Claims numeric_id doesn't exist... ?
        return issubclass(other, Channel) and self.numeric_id.__eq__(other.numeric_id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}<name : {self.name}, id : {self.numeric_id}, type : {self.type}, " \
               f"permissions : {self.permissions}> "

    def syncChannel(self, data):
        self.name = data["name"]
        self.numeric_id = data["channelId"]
        self.numeric_server_id = data["server_id"]

        self.alpha_numeric_id = data.get("_id")
        self.alpha_numeric_server_id = data.get("server")
        self.icon = data.get("icon")

        # A bit weird, needs thinking, empty permission object not possible as alpha_numeric_id is needed
        self.permissions = None if "permissions" not in data else Permissions.ChannelPermission(data["permissions"])
        self.rate_limit = data.get("rate_limit")
        self.type = data.get("type", 1)


# Only diff is text channel has `lastMessage`
class TextChannel(Channel):
    def __init__(self, data, header):
        super().__init__(data, header)

        self.lastMessaged = None
        self.messages = []

    def syncTextChannel(self, data):
        self.lastMessaged = data.get("lastMessaged")

    def addMessage(self, message):
        self.messages.append(message)

    def getMessage(self, messageId: str):
        return next((message for message in self.messages if message.message_numeric_id == messageId), None, )


class Category(Channel):
    def __init__(self, data, header):
        super().__init__(data, header)
