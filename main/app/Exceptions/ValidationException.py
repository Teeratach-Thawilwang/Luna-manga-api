from rest_framework import status


class ValidationException(Exception):
    def __init__(self, messages):
        self.messages = {"error": "Validation Exception.", "messages": [], "code": status.HTTP_422_UNPROCESSABLE_ENTITY}
        for key, values in messages.items():
            self.messages["messages"].append({key: str(values[0])})
        super().__init__(self.messages)
