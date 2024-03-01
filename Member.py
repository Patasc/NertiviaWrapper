class Member:
    def __init__(self, data, user, roles, header):
        self.server_numeric_id = None
        self.roles = roles
        self.type = None
        self.user = user

        self.header = header

        self.syncMember(data)

    def __repr__(self):
        return f"Member<server_id : {self.server_numeric_id}, type : {self.type}, user : {self.user}, roles : {self.roles}>"

    def __eq__(self, other):
        return isinstance(other, Member) and self.server_numeric_id.__eq__(other.server_numeric_id) and self.user.__eq__(other.user)

    def syncMember(self, data):
        self.server_numeric_id = data["server_id"]
        self.type = data.get("TYPE", "MEMBER")

    @property
    def numeric_id(self):
        return self.user.numeric_id

