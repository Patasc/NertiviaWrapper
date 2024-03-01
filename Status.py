class Status:
    def __init__(self, data):
        self.presence = 0
        self.custom_status = None

    def __repr__(self):
        return f"Status<presence: {self.presence}{'' if self.custom_status is None else ', custom : ' + self.custom_status}>"

    def syncStatus(self, data):
        # TODO: Deal with custom program status
        self.presence = data.get("status", 0)
        self.custom_status = data.get("custom")
