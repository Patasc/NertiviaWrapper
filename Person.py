import Status

# defaultAboutMe = {"_id": None, "gender": None, "age": None, "continent": None, "country": None, "about_me": None}

"""
We can access user data with HTTP requests if :
Friend
Server is Shared

Data obtained is in Dev/GetUserInfo.json
"""


class Person:
    def __init__(self, data, header):
        self.alpha_numeric_id = None  # Not given if not fetched
        self.numeric_id = None
        self.tag = None
        self.username = None

        self.avatar = None
        self.status = None  # Only obtainable on startup or updates, cannot be fetched

        self.bot = False  # Only obtainable on startup or updates, cannot be fetched

        self.about = {}  # Not given if None

        self.is_blocked = None

        self.header = header

        self.syncPerson(data)

    def __str__(self):
        return f"{self.username}:{self.tag}"

    def __repr__(self):
        return f"{self.__class__.__name__}<id : {self.numeric_id}, tag : {self.tag}>"

    def syncPerson(self, data):
        self.numeric_id = data["id"]
        self.tag = data["tag"]
        self.username = data["username"]

        self.alpha_numeric_id = data.get("_id")

        self.about = data.get("about", {})
        self.avatar = data.get("avatar")
        self.bot = data.get("bot", False)

    def update_status(self, data):
        self.status = Status.Status(data)


class User(Person):
    def __init__(self, data, header):
        super().__init__(data, header)

        self.banner = None  # Not given if not fetched

        # Contains numeric id
        self.common_friends = []
        self.common_servers = []

        self.syncUser(data)

    def __eq__(self, other):
        return isinstance(other, User) and other.numeric_id == self.numeric_id

    def syncUser(self, data):
        self.banner = data.get("banner")

        # Technically, common servers can be obtained for bots too, but doesn't seem pertinent ?
        self.common_friends = data.get("friends", [])  # Needs to be fetched if desired
        self.common_servers = data.get("servers", [])


class Bot(Person):
    def __init__(self, data, header):
        super().__init__(data, header)

        self.bot_prefix = None

    def syncBot(self, data):
        self.bot_prefix = data.get("botPrefix")
