class CollectionInvalidException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Image Collection Invalid."}
        for key, values in messages.items():
            self.messages = {**self.messages, **{key: str(values)}}
        super().__init__(self.messages)
