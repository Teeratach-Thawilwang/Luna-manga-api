from datetime import timedelta

from django.conf import settings
from django.core.cache import cache

from app.Notifications.EmailNotification import EmailNotification
from app.Services.EmailService import EmailService


class CustomerRegisterEmailNotification:
    def __init__(self, customer):
        self.customer = customer
        self.subject = "Welcome to Luna manga, ยินดีต้อนรับสู่ Luna manga"

        params = {
            "subject": self.subject,
            "template": "CustomerRegister/CustomerRegister.html",
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
            "confirm_link": EmailService().buildConfirmEmailLink(self.customer),
            "css": self.css(),
        }

    def css(self):
        contents = cache.get("customer_register_css")
        if contents is not None:
            return contents
        with open(settings.TEMPLATES_DIR + "CustomerRegister/CustomerRegister.css") as file:
            contents = file.read()
            timeout = timedelta(days=1).total_seconds()
            cache.set("customer_register_css", contents, timeout=timeout)
        return contents

    def buildTaskName(self):
        return "send_register_email_to_" + self.customer.email
