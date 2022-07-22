from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import config
from models.notification.notification import Notification


class NotificationSender:
    def send_notification(self, notification: Notification):
        pass


class Whatsapp(NotificationSender):
    pass


class Email(NotificationSender):
    def send_notification(self, notification):
        data = notification.get_email_data()

        message = Mail(from_email=config.sendgrid_email, to_emails=data["to"])
        message.dynamic_template_data = data["template_data"]
        message.template_id = data["template_id"]
        try:
            sg = SendGridAPIClient(config.sendgrid_key)
            sg.send(message)
            return True
        except Exception as e:
            return False


def get_sender(name):
    if name == "whatsapp":
        return Whatsapp()
    elif name == "email":
        return Email()
    else:
        raise Exception("Sender not found")
