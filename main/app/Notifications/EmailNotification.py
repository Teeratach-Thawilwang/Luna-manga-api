from app.Enums.QueueGroupEnum import QueueGroupEnum
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from django_q.tasks import async_task


class EmailNotification:
    def __init__(self, subject, template, message, recipients, files=[], taskName=None):
        params = {
            "subject": subject,
            "template": template,
            "message": message,
            "recipients": recipients,
            "files": files,
        }

        options = {
            "task_name": taskName or "Send Register Email",
            "group": QueueGroupEnum.SEND_MAIL,
        }
        async_task("app.Notifications.EmailNotification.EmailNotification.send", params=params, q_options=options)

    @staticmethod
    def send(params):
        templatePath = settings.TEMPLATES_DIR + params["template"]
        body = loader.render_to_string(templatePath, params["message"])

        mail = EmailMessage(
            subject=params["subject"],
            body=body,
            to=params["recipients"],
        )

        mail.content_subtype = "html"

        for file in params["files"]:
            path = settings.STORAGE_DIR + "/" + file
            mail.attach_file(path)

        mail.send()
