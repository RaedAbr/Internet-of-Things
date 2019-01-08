var iotdata = new AWS.IotData({endpoint: 'a72x50k0riqjj-ats.iot.eu-west-1.amazonaws.com'});

const lamp = document.getElementById("lamp");
const lampStateDiv = document.getElementById("lamp-state-div");
const switchDiv = document.getElementById("switch-div");
const loaderDivLamp = document.getElementById("loader-div-lamp");
const ledCheckbox = document.getElementById("led-checkbox");
const currentStateSpan = document.getElementById("current-state");
const desiredStateSpan = document.getElementById("desired-state");

// LED state requested from the user
let desiredLedState = "0";
// True if it's the first time the user open tha web page
let lampFirstTime = true;
// Dictionary of LED state for pretty display
const stateString = {"1": "ON", "0": "OFF"};

// Change the led state
function changeLedState(state) {
    if (lampFirstTime) {
        desiredLedState = state;
        lampFirstTime = false;
        lampStateDiv.style.display = "block";
        desiredStateSpan.textContent = stateString[desiredLedState];
        currentStateSpan.textContent = stateString[state];
    }
    if (desiredLedState === state) {
        switchDiv.hidden = false;
        loaderDivLamp.hidden = true;
        if (state == "1") {
            ledCheckbox.checked = true;
            lamp.style.backgroundPositionX = "-52px";
        } else {
            ledCheckbox.checked = false;
            lamp.style.backgroundPositionX = "4px";
        }
        currentStateSpan.textContent = stateString[state];
    }
}

// Notify user that LED state is pending
function pending(state) {
    desiredLedState = state;
    desiredStateSpan.textContent = stateString[desiredLedState];
    switchDiv.hidden = true;
    loaderDivLamp.hidden = false;
}

// Event handler for changing LED state request by checking/unchecking the checkbox
function changeLedStateRequest(checkbox) {
    desiredLedState = "0";
    if (checkbox.checked) {
        desiredLedState = "1";
    }
    websocket.send(JSON.stringify({action: "requestState", state: desiredLedState}));
    publish();
}

// Publish a downlink
function publish() {
    let payloadJson = '{"port": 1,"confirmed": false,"payload_raw": "' + btoa(desiredLedState) + '"}',  /* btoa convert string to base64 */
        waspmoteTtnTopic = 'iot_2018_19_abdennadher_gindre/devices/waspmote_0/down';
    let params = {
        topic: waspmoteTtnTopic,
        payload: payloadJson,
        qos: 0
    };
    iotdata.publish(params, function(err, data) {
        if (err) {
            // an error occurred
            logging(err.stack);
        } else {
            // successful response
            logging("publish: " + payloadJson + " to topic: " + waspmoteTtnTopic);
        }
    });
}
