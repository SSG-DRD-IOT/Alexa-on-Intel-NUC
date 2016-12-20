'use strict';
var config = {};

config.IOT_BROKER_ENDPOINT      = "a2la7zf3kffmrf.iot.us-east-1.amazonaws.com".toLowerCase();

config.IOT_BROKER_REGION        = "us-east-1";


//Loading AWS SDK libraries

var AWS = require('aws-sdk');

AWS.config.region = config.IOT_BROKER_REGION;

//Initializing client for IoT

var iotData = new AWS.IotData({endpoint: config.IOT_BROKER_ENDPOINT});

var Alexa = require('alexa-sdk');
var APP_ID = undefined; //OPTIONAL: replace with 'amzn1.echo-sdk-ams.app.[your-unique-value-here]';
var SKILL_NAME = 'gateway demo';

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var blue_state = 0;
var red_state = 0;

var handlers = {
    'LaunchRequest': function () {

      var deviceState = [
        {"state":{ "desired":{"device":"NUC-Gateway","red_led":0,"blue_led":0}}}
      ];
      var speechOutput="Gateway Operational";
      AWSIoT.sendMessage(this, deviceState,speechOutput);

    },
    'DeviceStateIntent': function () {

      var speechOutput;
      var itemSlot = this.event.request.intent.slots.DeviceState;
      console.log("itemSlot: "+itemSlot);
      var Device_States="none";
      if (itemSlot && itemSlot.value) {
          Device_States = itemSlot.value.toLowerCase();
      }
      console.log("Device_States: "+Device_States);
      var deviceState=null;

      switch (Device_States) {
        case "all on":
        blue_state = 1;
        red_state = 1;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="all on";
        break;
        case "all off":
        blue_state = 0;
        red_state = 0;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="all off";
        break;
        case "blue led on":
        blue_state = 1;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="blue L E D on";
        break;
        case "red led on":
        red_state = 1;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="red L E D on";
        break;
        case "none":
        default:
        speechOutput="no device state";
        break;
        case "red led off":
        red_state = 0;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="red L E D off";
        break;
        case "blue led off":
        blue_state = 0;
        deviceState = [
        {'state':{ 'desired':{'device':'NUC-Gateway','red_led':red_state,'blue_led':blue_state}}}
        ];
        speechOutput="blue L E D off";
        break;
      }
      if (deviceState==null) {
        this.emit(':tell',speechOutput);
      } else {
        AWSIoT.sendMessage(this, deviceState, speechOutput);
      }


    },
    'AMAZON.HelpIntent': function () {
        this.attributes['speechOutput'] = 'You can ask questions such as, what\'s the device state, or, you can say exit... ' +
            'Now, what can I help you with?';
        this.attributes['repromptSpeech'] = 'You can say things like, what\'s the device satate, or you can say exit...' +
            ' Now, what can I help you with?';
        this.emit(':ask', this.attributes['speechOutput'], this.attributes['repromptSpeech'])
    },
    'AMAZON.RepeatIntent': function () {
        this.emit(':ask', this.attributes['speechOutput'], this.attributes['repromptSpeech'])
    },
    'AMAZON.StopIntent': function () {
        this.emit('SessionEndedRequest');
    },
    'AMAZON.CancelIntent': function () {
        this.emit('SessionEndedRequest');
    },
    'SessionEndedRequest':function () {
        this.emit(':tell', 'Goodbye!');
    }
  };
var AWSIoT = {
    postSendMessage: function (thisOfParent,speechOutput) {
      console.log('all done');
      thisOfParent.emit(':tell', speechOutput);
    },
    sendMessage: function (thisOfParent, deviceState, speechOutput) {

      var itemsProcessed = 0;

      //var deleteme = {'state':{ 'desired':{'percent_on':0,'color':'blue','device':'light1','type':'light','state':'locked'}}};
      deviceState.forEach((item, index, array) => {


          console.log("item "+index+": "+JSON.stringify(item));
          console.log("device "+index+": "+item.state.desired.device)

          var thingNameAndPayload= {
            "thingName" : item.state.desired.device,
            "payload" : JSON.stringify(item)
          };
          iotData.updateThingShadow(thingNameAndPayload, function(err, data) {

            if (err){
              console.log("update error: ");
              console.log(err);
              //Handle the error here
              speechOutput = "error updating device state";
              //thisOfParent.emit(':tell', speechOutput);
            }

            else {
              console.log("update success: ");
              console.log(data);
              //callback(sessionAttributes,buildSpeechletResponse(intent.name, speechOutput, repromptText, shouldEndSession));
              //thisOfParent.emit(':tell', speechOutput);
            }
          itemsProcessed++;
          if(itemsProcessed === array.length) {
              AWSIoT.postSendMessage(thisOfParent, speechOutput);
            }


          });

        });

    }

  };
