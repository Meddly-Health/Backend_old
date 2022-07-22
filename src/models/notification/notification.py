class Notification:
    def __init__(self, contact_data, **kwargs):
        """
        contact_data:
        {
            "whatsapp": "123456789",
            "email": "test@test.com"
        }
        """
        self.contact_data = contact_data

    def get_whatsapp_data(self):
        """
        Returns an object the following format:
        {
            "to": "123456789",
            "message": "Hello World!"
        }
        """
        pass

    def get_email_data(self):
        """
        Returns an object the following format:
        {
            "to": "test@example.com",
            "template_id": "d-a5ff5b76bb8443beb7e4192b6c6e6863"
            "template_data": { ... }
        }
        """
        pass


class NewSupervisorNotification(Notification):
    def __init__(self, user, **kwargs):
        super().__init__(user, **kwargs)
        self.supervisor_name = kwargs["supervisor_name"]

    def get_whatsapp_data(self):
        if self.supervisor_name:
            message = f"Se ha agregado a {self.supervisor_name} como supervisor."
        else:
            message = "Se ha agregado a un nuevo supervisor."

        return {"to": self.contact_data["whatsapp"], "message": message}

    def get_email_data(self):
        template_id = "d-5e634cd5cd6548b4b440f188c1d2a40a"
        return {
            "to": self.contact_data["email"],
            "template_id": template_id,
            "template_data": {"supervisor_name": self.supervisor_name},
        }


class ReminderTakeMedsNotification(Notification):
    def get_whatsapp_data(self):
        print("Sending reminder to take meds to whatsapp")

    def get_email_data(self):
        print("Sending reminder to take meds to email")
