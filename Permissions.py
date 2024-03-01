class RolePermission:
    def __init__(self, permissions: int):
        self.admin = False
        self.ban = False
        self.kick = False
        self.manage_channels = False
        self.manage_roles = False
        self.send_messages = False

        self.syncPermission(permissions)

    def syncPermission(self, permissions):

        # Can this be cleaned up ?
        # No switch for python < 3.10
        if permissions % 32 == 1:
            permissions -= 32
            self.ban = True

        if permissions % 16 == 1:
            permissions -= 16
            self.kick = True

        if permissions % 8 == 1:
            permissions -= 8
            self.manage_channels = True

        if permissions % 4 == 1:
            permissions -= 4
            self.manage_roles = True

        if permissions % 2 == 1:
            permissions -= 2
            self.send_messages = True

        if permissions % 1 == 1:
            self.admin = True


class ChannelPermission:
    def __init__(self, data):
        self.alpha_numeric_id = None
        self.send_message = None

        self.syncPermission(data)

    def __repr__(self):
        return f"ChannelPermission<_id : {self.alpha_numeric_id}, sendMessage : {self.send_message}>"

    def __eq__(self, other):
        # IDE claims alpha_numeric_id doesn't exist ?
        return isinstance(other, ChannelPermission) and self.alpha_numeric_id.__eq__(other.alpha_numeric_id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def syncPermission(self, data):
        # Only channel permissions are given an id ?
        self.alpha_numeric_id = data.get("_id")
        self.send_message = data.get("send_message", False)
