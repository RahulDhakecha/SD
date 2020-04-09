import smtplib, ssl
import os

# port = 465  # For SSL
# # password = input("Type your password and press enter: ")
# sender_email = "business.dev.rajgroup@gmail.com"
# password = "Raj.business123"
# receiver_email = "rahuldhakecha1311@gmail.com"
# message = """\
# Subject: Hi there
#
# This message is sent from Python."""
#
# # Create a secure SSL context
# context = ssl.create_default_context()
#
# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("business.dev.rajgroup@gmail.com", password)
#     server.sendmail(sender_email, receiver_email, message)


class GMailConn:

    def __init__(self, sender=os.environ.get("SENDER_EMAIL"), password=os.environ.get("SENDER_PASSWORD"),
                 port=os.environ.get("EMAIL_PORT")):
        self.sender = sender
        password = password
        port = port
        context = ssl.create_default_context()
        self.email_server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        self.email_server.login(sender, password)

    def send_email(self, receiver_email=None, subject=None, message=None):
        complete_message = "Subject:"+subject+"\n\n"+message
        print(complete_message)
        self.email_server.sendmail(self.sender, receiver_email, complete_message)


if __name__ == "__main__":
    gmailconn = GMailConn()
    gmailconn.send_email(receiver_email="rahuldhakecha1311@gmail.com", subject="REMINDER: Offer Pending", message="Offer is pending for project")
