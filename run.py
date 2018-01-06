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
	response.say("What is cracking fool?")
	# response.play("/audio/beep.wav")
	response.record(maxLength=30, timeout=5, transcribeCallback="/transcribe")
	response.hangup()
	return str(response)

# this one sends texts
@app.route("/transcribe", methods=["GET", "POST"])
def sendSentiment():
	my_number = "+14155551234"
	app_number = "+15105554321"
	dummy = request.form 
	caller_number, text = request.form['From'], request.form['TranscriptionText']
	#text = dummy['TranscriptionText']
	#text = "good"
	sentiment = analyzeSentiment(text)
	#sentiment = "angry"
	body_text = 'Caller at ' + caller_number + ' is ' + sentiment + " : " + text
	message = client.messages.create(
		my_number,
		body=body_text,
		from_=app_number)
	print(message.sid)
	return str(message)

# run
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host="0.0.0.0", port=port)
