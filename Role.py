import Permissions


# Cannot be fetched, only obtainable from events
class Role:
    def __init__(self, data, header):
        self.name = None
        self.permissions = None
        self.default = None
        self.deletable = None
        self.numeric_id = None
        self.bot = None
        self.server_numeric_id = None
        self.order = None
        self.hide_role = None

        self.header = header

        self.syncRole(data)

    def __repr__(self):
        return f"Role<id : {self.numeric_id}, name : {self.name}, order : {self.order}, permissions : {self.permissions}>"

    def __eq__(self, other):
        return isinstance(other, Role) and self.numeric_id.__eq__(other.numeric_id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, Role):
            other = other.order
        if isinstance(other, int):
            return self.numeric_id.__gt__(other)
        return False  # Not raising an error in case of incompatible types, keep ?

    def __lt__(self, other):
        return other.__gt__(self) if isinstance(other, Role) else False

    def syncRole(self, data):
        self.name = data["name"]
        self.default = data.get("default", False)
        self.deletable = data.get("deletable", False)
        self.numeric_id = data["id"]
        self.bot = data.get("bot")
        self.server_numeric_id = data["server_id"]
        self.order = data["order"]
        self.hide_role = data.get("hideRole", False)

        self.permissions = Permissions.RolePermission(data.get("permissions", 0))
