class Notification:
    def send_whatsapp(self):
        pass

    def send_email(self):
        pass


class NewSupervisor(Notification):
    def send_whatsapp(self):
        print("Sending new supervisor notification to whatsapp")

    def send_email(self):
        print("Sending new supervisor notification to email")


class ReminderTakeMeds(Notification):
    def send_whatsapp(self):
        print("Sending reminder to take meds to whatsapp")

    def send_email(self):
        print("Sending reminder to take meds to email")
