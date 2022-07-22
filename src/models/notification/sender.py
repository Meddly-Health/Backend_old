class NotificationSender:
    def send_notification(self, message):
        pass


class Whatsapp(NotificationSender):
    pass


class Email(NotificationSender):
    pass


def get_sender(name):
    if name == "whatsapp":
        return Whatsapp()
    elif name == "email":
        return Email()
    else:
        raise Exception("Sender not found")
