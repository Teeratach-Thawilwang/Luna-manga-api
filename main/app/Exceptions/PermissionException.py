class PermissionException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Permission Exception."}
        for key, values in messages.items():
            self.messages = {**self.messages, **{key: str(values)}}
        super().__init__(self.messages)
