var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
   keyPath: "NUC-Gateway.private.key",
  certPath: "NUC-Gateway.cert.pem",
    caPath: "root-CA.crt",
  clientId: "arn:aws:iot:us-east-1:089742002813:thing/NUC-Gateway",
    region: "us-east-1"
});

device
  .on('connect', function() {
    console.log('connected to device...');
    device.subscribe('$aws/things/NUC-Gateway/shadow/update/accepted')

    //device.publish('topic', JSON.stringify({ test_data: 1}));
    });

device
  .on('message', function(topic, payload) {
    string_payload = payload.toString();
    json_payload = JSON.parse(string_payload);

    console.log('blue led state: ', topic, json_payload.state.desired.blue_led);
    console.log('red led state: ', topic, json_payload.state.desired.red_led);


  });
