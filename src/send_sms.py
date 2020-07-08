# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACf46189a9ceca2b697f802f912661f127'
auth_token = 'd294e42e19c2fedc65a006946efe8fa7'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12029521329',
                     to='+14147952004'
                 )

print(message.sid)