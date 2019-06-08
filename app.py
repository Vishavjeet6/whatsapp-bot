from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import getReply
from twilio.rest import Client

account_sid = 'AC333441095fba29a974eb2f0d909f8676'
auth_token = 'ff86176bbb58a61ccd09444f3c2bafe7'
t_client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    resp.message(getReply(msg, sender))
    return (str(resp))

if __name__ == "__main__":
    app.run(debug=True)