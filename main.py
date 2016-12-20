#! /usr/bin/env python
from PyMata.pymata import PyMata

import subprocess
import os
import random
import time
import alsaaudio
import wave
import random
from creds import *
import requests
import json
import re
from memcache import Client

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

myMQTTClient = AWSIoTMQTTClient("arn:aws:iot:us-east-1:089742002813:thing/NUC-Gateway")
myMQTTClient.configureEndpoint("a2la7zf3kffmrf.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("root-CA.crt", "NUC-Gateway.private.key", "NUC-Gateway.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()

Button = 8
LED_Status = 3
LED_Record = 4
blue_led = 5;
red_led = 6;

board = PyMata("/dev/ttyACM0", verbose=True)

board.set_pin_mode(LED_Status, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(LED_Record, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(Button, board.INPUT, board.DIGITAL)

def customCallback(client, userdata, message):
    print("Received a new message: ")
    parsed_json = json.loads(message.payload)
    blue_led_state = parsed_json["state"]["desired"]["blue_led"]
    red_led_state = parsed_json["state"]["desired"]["red_led"]
    print(blue_led_state)
    print(red_led_state)
    board.digital_write(blue_led, blue_led_state)
    board.digital_write(red_led, red_led_state)

#Setup
recorded = False
servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))

def internet_on():
    print "Checking Internet Connection"
    try:
        r =requests.get('https://api.amazon.com/auth/o2/token')
	print "Connection OK"
        return True
    except:
	print "Connection Failed"
    	return False


def gettoken():
	token = mc.get("access_token")
	refresh = refresh_token
	if token:
		return token
	elif refresh:
		payload = {"client_id" : Client_ID, "client_secret" : Client_Secret, "refresh_token" : refresh, "grant_type" : "refresh_token", }
		url = "https://api.amazon.com/auth/o2/token"
		r = requests.post(url, data = payload)
		resp = json.loads(r.text)
		mc.set("access_token", resp['access_token'], 3570)
		return resp['access_token']
	else:
		return False


def alexa():
        print 'alexa function called'
	board.digital_write(LED_Status, 1)
	url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
	headers = {'Authorization' : 'Bearer %s' % gettoken()}
	d = {
   		"messageHeader": {
       		"deviceContext": [
           		{
               		"name": "playbackState",
               		"namespace": "AudioPlayer",
               		"payload": {
                   		"streamId": "",
        			   	"offsetInMilliseconds": "0",
                   		"playerActivity": "IDLE"
               		}
           		}
       		]
		},
   		"messageBody": {
       		"profile": "alexa-close-talk",
       		"locale": "en-us"#,
#       		"format": "audio/L16; rate=16000; channels=1"
   		}
	}
	with open(path+'recording.wav') as inf:
                print 'with open recording.wav'
		files = [
				('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
				('file', ('audio', inf, 'audio/L16; rate=16000; channels=1'))
				]
		r = requests.post(url, headers=headers, files=files)
                print r.status_code
	if r.status_code == 200:
                print 'status code 200'
		for v in r.headers['content-type'].split(";"):
			if re.match('.*boundary.*', v):
                                print 'if re.match'
				boundary =  v.split("=")[1]
		data = r.content.split(boundary)
		for d in data:
                        print 'for d in data'
			if (len(d) >= 1024):
				audio = d.split('\r\n\r\n')[1].rstrip('--')
		with open(path+"response.mp3", 'wb') as f:
			f.write(audio)
		board.digital_write(LED_Record, 0)
		os.system('mpg123 -q {}1sec.mp3 {}response.mp3'.format(path, path))
		board.digital_write(LED_Status, 0)

	else:
                print 'else, no code 200'
		board.digital_write(LED_Record, 0)
		board.digital_write(LED_Status, 0)
		for x in range(0, 3):
			time.sleep(.2)
			board.digital_write(LED_Record, 1)
			time.sleep(.2)
			board.digital_write(LED_Record, 0)
			board.digital_write(LED_Status, 0)




def start():
    recording = 0
    last = 0
    while True:

        val =  board.digital_read(Button)
        if val == 1 and last == 0:
            last = 1;
            record = subprocess.Popen(['arecord', '-r', '16000', '-f', 'S16_LE', '--period-size', '500', '-c', '1', '-vv', 'recording.wav'])
            recording = 1;
            board.digital_write(LED_Record, 1)
        elif val == 0 and recording == 1:
            last = 0;
            recording = 0;
            record.kill()
            board.digital_write(LED_Record, 0)
            myMQTTClient.subscribe("$aws/things/NUC-Gateway/shadow/update/accepted", 1, customCallback)
            alexa()


if __name__ == "__main__":


	board.digital_write(LED_Status, 0)
	board.digital_write(LED_Record, 0)

	while internet_on() == False:
		print "."
	token = gettoken()
	os.system('mpg123 -q {}1sec.mp3 {}hello.mp3'.format(path, path))
	for x in range(0, 3):
		time.sleep(.1)
		board.digital_write(LED_Status, 1)
		time.sleep(.1)
		board.digital_write(LED_Status, 0)
	start()
