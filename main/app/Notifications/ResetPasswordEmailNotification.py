from datetime import timedelta

from app.Notifications.EmailNotification import EmailNotification
from app.Services.EmailService import EmailService
from django.conf import settings
from django.core.cache import cache


class ResetPasswordEmailNotification:
    def __init__(self, customer):
        self.customer = customer
        self.subject = "Reset Password, รีเซ็ตรหัสผ่าน"

        params = {
            "subject": self.subject,
            "template": "ResetPassword/ResetPassword.html",
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
            "reset_password_link": EmailService().buildResetPasswordLink(self.customer),
            "css": self.css(),
        }

    def css(self):
        contents = cache.get("reset_password_css")
        if contents is not None:
            return contents
        with open(settings.TEMPLATES_DIR + "ResetPassword/ResetPassword.css") as file:
            contents = file.read()
            timeout = timedelta(days=1).total_seconds()
            cache.set("reset_password_css", contents, timeout=timeout)
        return contents

    def buildTaskName(self):
        return "send_reset_password_to_" + self.customer.email
