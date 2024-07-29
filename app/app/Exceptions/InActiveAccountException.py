class InActiveAccountException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Inactive Account."}
        for key, values in messages.items():
            self.messages = {**self.messages, **{key: str(values)}}
        super().__init__(self.messages)
