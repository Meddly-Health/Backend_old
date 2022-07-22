from database import Database
from models.notification.sender import get_sender


class NotificationManager:
    def __init__(self, active_notifications):
        self.senders = get_sender(active_notifications)

    def get_senders(self, active_notifications):
        return [get_sender(name) for name in active_notifications]

    def send_notification(self, message):
        for sender in self.senders:
            sender.send_notification(message)


async def get_manager(user):
    db = await Database.get_db()
    active_notifications = db["user"].find_one(
        {"_id": user["user_id"]}, {"active_notifications": 1}
    )
    return NotificationManager(active_notifications["active_notifications"])
