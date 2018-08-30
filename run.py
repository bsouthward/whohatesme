import os
import sys
from flask import Flask, request, redirect, copy_current_request_context
from twilio.twiml.voice_response import Record, VoiceResponse
from twilio.rest import Client
from config import account_sid, auth_token
from analyze_sentiment import *

# set up a Client and a Flask app
client = Client(account_sid, auth_token)

app = Flask(__name__)

# this one receives calls
@app.route("/", methods=['GET', 'POST'])
def record():
	response = VoiceResponse()
	response.say("What's cracking, fool?", loop=1)
	# response.play("/audio/beep.wav")
	response.record(max_length=30, timeout=30, action="/hangup", 
		transcribe_callback="/transcribe")
	response.hangup()
	return str(response)

# this one sends texts
@app.route("/transcribe", methods=["GET", "POST"])
def sendSentiment():
	dummy = request.form 
	caller_number, text = request.form['From'], request.form['TranscriptionText']
	#text = dummy['TranscriptionText']
	#text = "good"
	sentiment = analyzeSentiment(text)
	#sentiment = "angry"
	body_text = 'Caller at ' + caller_number + ' is ' + sentiment + " : " + text
	message = client.messages.create(
		"+15125341001",
		body=body_text,
		from_="+15046669635")
	print(message.sid)
	return str(message)

# hang up
@app.route("/hangup", methods=["GET", "POST"])
def hangUp():
	response = VoiceResponse()
	response.hangup()
	return str(response)

# run
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host="0.0.0.0", port=port)
