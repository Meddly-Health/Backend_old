import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

try:
    import set_environ
except ModuleNotFoundError:
    pass
from config import sendgrid_key


def send_dynamic(template_id, send_to, template_data):
    """Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception"""
    # create Mail object and populate
    message = Mail(from_email="meddly.health@gmail.com", to_emails=send_to)
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = template_data
    message.template_id = template_id
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(sendgrid_key)
        sg.send(message)
        print("Dynamic Message Sent!")
    except Exception as e:
        print("Error: {0}".format(e))


if __name__ == "__main__":
    send_to = [("soficibello@gmail.com", "Ignacio Pieve")]
    send_dynamic("d-a5ff5b76bb8443beb7e4192b6c6e6863", "soficibello@gmail.com", {})
