import jwt
from app.Domain.Configuration.Services.ConfigurationService import ConfigurationService
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.ConfirmEmailInvalidException import ConfirmEmailInvalidException
from app.Exceptions.EmailExpiredException import EmailExpiredException
from app.Exceptions.ResetPasswordInvalidException import ResetPasswordInvalidException
from django.utils import timezone


class EmailService:
    def decode(self, code, configKey):
        secret = ConfigurationService().findByKey(configKey).value
        payload = jwt.decode(code.encode("utf-8"), secret, algorithms="HS256")

        if "secret" not in payload:
            return None

        if "customer_id" not in payload:
            return None

        if "customer_email" not in payload:
            return None

        if secret != payload["secret"]:
            return None

        return payload

    def buildConfirmEmailLink(self, customer):
        link = ConfigurationService().findByKey("customer_register_confirm_email_link").value
        secret = ConfigurationService().findByKey("customer_register_confirm_email_secret").value

        payload = {
            "customer_id": customer.id,
            "customer_email": customer.email,
            "secret": secret,
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        return link + "?code=" + token

    def getVerifiedCustomerFromCode(self, code):
        try:
            payload = self.decode(code, "customer_register_confirm_email_secret")
        except Exception as e:
            raise ConfirmEmailInvalidException({"message": e})

        if payload is None:
            return None

        return CustomerService().findBy({"id": payload["customer_id"], "email": payload["customer_email"]}).first()

    def buildResetPasswordLink(self, customer):
        link = ConfigurationService().findByKey("customer_reset_password_link").value
        secret = ConfigurationService().findByKey("customer_reset_password_secret").value
        expiredAt = timezone.now() + timezone.timedelta(minutes=20)
        payload = {
            "customer_id": customer.id,
            "customer_email": customer.email,
            "secret": secret,
            "expired_at": expiredAt.timestamp(),
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        return link + "?code=" + token

    def getCustomerFromResetPasswordCode(self, code):
        try:
            payload = self.decode(code, "customer_reset_password_secret")
        except Exception as e:
            raise ResetPasswordInvalidException({"message": e})

        if payload is None:
            return None

        if payload["expired_at"] < timezone.now().timestamp():
            raise EmailExpiredException({"message": "Email Expired."})

        return CustomerService().findBy({"id": payload["customer_id"], "email": payload["customer_email"]}).first()
