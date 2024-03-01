import Channel
import Role
import Member


class Server:
    def __init__(self, data, header):
        self.name = None
        self.alpha_numeric_id = None
        self.numeric_id = None

        self.avatar = None
        self.channel_positions = None

        self.creator = None
        self.default_channel_numeric_id = None

        self.channels = None
        # Only obtainable via fetch
        self.created = None
        self.members = {}
        self.roles = {}

        self.header = header

        self.sync_server(data)

    def __eq__(self, other):
        return isinstance(other, Server) and self.numeric_id.__eq__(other.numeric_id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}<id : {self.numeric_id}, {'' if self.creator is None else 'creator : ' + self.creator + ', '}channels : {self.channels}> "

    def sync_server(self, data):
        self.avatar = data["avatar"]
        self.default_channel_numeric_id = data["default_channel_id"]
        self.name = data["name"]
        self.numeric_id = data["server_id"]

        self.alpha_numeric_id = data.get("_id")
        self.channel_positions = data.get("channel_position", [])

        self.channels = [Channel.TextChannel(i, self.header) if i.get("type", 1) == 1 else Channel.Category(i, self.header) for i in data.get("channels", [])]

        self.created = data.get("created")
        self.creator = data.get("creator", {}).get("id")

    def add_role(self, role: Role.Role):
        if not isinstance(role, Role.Role):
            return
        self.roles[role.numeric_id] = role

    def add_member(self, member: Member.Member):
        if not isinstance(member, Member.Member):
            return
        self.members[member.numeric_id] = member

    async def get_member(self, member_id):
        return self.members.get(member_id)

    async def get_role(self, role_id: str):
        return self.roles.get(role_id)

    def get_channel(self, channel_id):
        return next((channel for channel in self.channels if channel.numeric_id == channel_id ), None, )
