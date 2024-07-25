class TokenInvalidException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Token Invalid."}
        for key, values in messages.items():
            self.messages = {**self.messages, **{key: str(values)}}
        super().__init__(self.messages)
