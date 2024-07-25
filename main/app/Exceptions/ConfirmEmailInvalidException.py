class ConfirmEmailInvalidException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Confirm Email Invalid."}
        for key, values in messages.items():
            self.messages = {**self.messages, **{key: str(values)}}
        super().__init__(self.messages)
