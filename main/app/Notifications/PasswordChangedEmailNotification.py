from datetime import timedelta

from app.Notifications.EmailNotification import EmailNotification
from app.Services.EmailService import EmailService
from django.conf import settings
from django.core.cache import cache


class PasswordChangedEmailNotification:
    def __init__(self, customer):
        self.customer = customer
        self.subject = "Your password changed, เปลี่ยนรหัสผ่านสำเร็จแล้ว"

        params = {
            "subject": self.subject,
            "template": "PasswordChanged/PasswordChanged.html",
            "message": self.transformData(),
            "recipients": [self.customer.email],
            "files": [],
            "taskName": self.buildTaskName(),
        }
        EmailNotification(**params)

    def transformData(self):
        return {
            "first_name": self.customer.first_name,
            "last_name": self.customer.last_name,
            "email": self.customer.email,
            "css": self.css(),
        }

    def css(self):
        contents = cache.get("password_changed_css")
        if contents is not None:
            return contents
        with open(settings.TEMPLATES_DIR + "ResetPassword/ResetPassword.css") as file:
            contents = file.read()
            timeout = timedelta(days=1).total_seconds()
            cache.set("password_changed_css", contents, timeout=timeout)
        return contents

    def buildTaskName(self):
        return "send_password_changed_to_" + self.customer.email
