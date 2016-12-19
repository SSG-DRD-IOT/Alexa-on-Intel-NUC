# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

def customCallback(client, userdata, message):
    print("Received a new message: ")
    parsed_json = json.loads(message.payload)
    print(parsed_json["state"]["desired"]["blue_led"])



myMQTTClient = AWSIoTMQTTClient("arn:aws:iot:us-east-1:089742002813:thing/NUC-Gateway")

myMQTTClient.configureEndpoint("a2la7zf3kffmrf.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("root-CA.crt", "NUC-Gateway.private.key", "NUC-Gateway.cert.pem")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
while True:
    myMQTTClient.subscribe("$aws/things/NUC-Gateway/shadow/update/accepted", 1, customCallback)
