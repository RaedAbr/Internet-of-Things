console.log('Loading function');

// FILL IN YOUR SNS TOPIC ARN HERE
var topicArn = "arn:aws:sns:eu-west-1:166010466283:esp32_alarm_notification";

var AWS = require('aws-sdk');
AWS.config.region = 'eu-west-1';

exports.handler = function(event, context) {
    var sns = new AWS.SNS();
    
    let esp32Message = event;

    console.log("data received\n " + JSON.stringify(esp32Message));
    sns.publish({
        Message: 'High temperature was detected: ' + JSON.stringify(esp32Message),
        TopicArn: topicArn
    }, function(err, data) {
        if (err) {
            console.log(err.stack);
            return;
        }
        console.log('alarm notification send');
        console.log(data);
        context.done(null, 'Function Finished!');
    });
};
