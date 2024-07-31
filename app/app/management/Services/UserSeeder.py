from app.Domain.Authorization.Models.ModelHasRole import ModelHasRole
from app.Domain.Authorization.Models.Role import Role
from app.Domain.User.Models.User import User
from app.Domain.User.Models.UserFactory import UserFactory
from app.Enums.StatusEnum import UserStatusEnum
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType


class UserSeeder:
    def create(self, quality=1, isSuperUser=False):
        if isSuperUser:
            self.createSuperUser()
        else:
            self.createUser(quality)

    def createSuperUser(self):
        role = Role.objects.filter(name="super-admin").first()
        if role is None:
            params = {
                "guard_name": "back-office",
                "name": "super-admin",
                "description": "super-admin",
            }
            role = Role.objects.create(**params)

        email = settings.SUPER_USER_ADMIN_EMAIL
        password = settings.SUPER_USER_PASSWORD
        user = User.objects.filter(id=1, email=email).first()
        if user is None:
            params = {
                "id": 1,
                "email": email,
                "password": make_password(password),
                "nick_name": "super-user",
                "first_name": "super-user",
                "last_name": "super-user",
                "is_superuser": True,
                "status": UserStatusEnum.ACTIVE,
            }
            user = UserFactory.create(**params)

        userType = ContentType.objects.get_for_model(User)
        modelHasRole = ModelHasRole.objects.filter(role_id=role.id, model_id=user.id, model_type=userType).first()
        if modelHasRole is None:
            params = {
                "role_id": role.id,
                "model_id": user.id,
                "model_type": userType,
            }
            ModelHasRole.objects.create(**params)

        return user

    def createUser(self, quality):
        lastUserIndex = User.objects.values("id").last()["id"]
        for n in range(lastUserIndex + 1, lastUserIndex + 1 + quality):
            params = {
                "email": f"user-{n}@email.com",
                "password": make_password("user1234"),
                "status": UserStatusEnum.INACTIVE,
            }
            UserFactory.create(**params)
