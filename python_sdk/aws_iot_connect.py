# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload.state.desired.blue_led)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


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
