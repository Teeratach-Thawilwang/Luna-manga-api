from app.Domain.User.Models.UserFactory import UserFactory


class ExampleJob:
    def handle():
        params = {
            "password": "user1234",
        }
        user = UserFactory.create(**params)
        print(f"In ExampleJob create user with email : {user.email}")
