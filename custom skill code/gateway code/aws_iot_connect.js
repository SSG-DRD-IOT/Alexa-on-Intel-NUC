var mraa = require('mraa');
console.log('MRAA Version: ' + mraa.getVersion());

mraa.addSubplatform(mraa.GENERIC_FIRMATA, "/dev/ttyACM0");

var blue_led_pin = new mraa.Gpio(5);
var red_led_pin = new mraa.Gpio(6);

blue_led_pin.dir(mraa.DIR_OUT);
red_led_pin.dir(mraa.DIR_OUT);

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
    red_led_state = json_payload.state.desired.red_led;
    blue_led_state = json_payload.state.desired.blue_led;


    console.log('blue led state: ', topic, blue_led_state);
    console.log('red led state: ', topic, red_led_state);
    blue_led_pin.write(blue_led_state)
    red_led_pin.write(red_led_state)


  });
