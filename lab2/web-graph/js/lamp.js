var iotdata = new AWS.IotData({endpoint: 'a72x50k0riqjj-ats.iot.eu-west-1.amazonaws.com'});

const lamp = document.getElementById("lamp");
const lampStateDiv = document.getElementById("lamp-state-div");
const switchDiv = document.getElementById("switch-div");
const loaderDiv = document.getElementById("loader-div");
const ledCheckbox = document.getElementById("led-checkbox");
const currentStateSpan = document.getElementById("current-state");
const desiredStateSpan = document.getElementById("desired-state");

let desiredLedState = "0";
let firstTime = true;
const stateString = {"1": "ON", "0": "OFF"};

websocket = new WebSocket("ws://63.33.115.200:6789/");

websocket.onmessage = function (event) {
    data = JSON.parse(event.data); // data in form {type: "waspmote", state: "1"}
    switch (data.type) {
        case 'waspmote':
            console.log(data);
            changeLedState(data.state);
            break;
        default:
            console.error("ignored", data);
    }
};

function changeLedState(state) {
    if (firstTime) {
        desiredLedState = state;
        firstTime = false;
        lampStateDiv.style.display = "block";
        desiredStateSpan.textContent = stateString[desiredLedState];
        currentStateSpan.textContent = stateString[state];
    }
    if (desiredLedState === state) {
        switchDiv.hidden = false;
        loaderDiv.hidden = true;
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

function changeLedStateRequest(checkbox) {
    if (checkbox.checked) {
        desiredLedState = "1";
    } else {
        desiredLedState = "0";
    }
    desiredStateSpan.textContent = stateString[desiredLedState];
    switchDiv.hidden = true;
    loaderDiv.hidden = false;
    publish();
}

function publish() {
    var params = {
        topic: 'iot_2018_19_abdennadher_gindre/devices/waspmote_0/down',
        payload: '{"port": 1,"confirmed": false,"payload_raw": "' + btoa(desiredLedState) + '"}'  /* btoa convert string to base64 */,
        qos: 0
    };
    iotdata.publish(params, function(err, data) {
        if (err) {
            console.log(err, err.stack); // an error occurred
        } else {
            console.log(data);           // successful response
        }
    });
}