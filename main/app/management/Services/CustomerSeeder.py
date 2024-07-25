from app.Domain.Customer.Models.Customer import Customer
from app.Enums.StatusEnum import CustomerStatusEnum
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class CustomerSeeder:
    def create(self):
        email = settings.CUSTOMER_ADMIN_EMAIL
        password = settings.CUSTOMER_ADMIN_PASSWORD
        customer = Customer.objects.filter(id=1, email=email).first()
        if customer is None:
            params = {
                "id": 1,
                "email": email,
                "password": make_password(password),
                "nick_name": "admin",
                "first_name": "admin",
                "last_name": "admin",
                "status": CustomerStatusEnum.ACTIVE,
                "email_verified_at": timezone.now(),
            }
            customer = Customer.objects.create(**params)
