// Establish websocket secure connection
var websocket = new WebSocket("wss://iot-course-master.tk:6789/");

// Invoked when error occurs 
websocket.onerror = function (event) {  
    logging("Error");
}

// Invoked when receiving message from websocket server
websocket.onmessage = function (event) {
    data = JSON.parse(event.data); 
    switch (data.type) {
        case 'led': 
            // Receiving message containting new LED status
            // in form {type: "led", state: "1"}
            logging(data);
            changeLedState(data.state);
            break;
        case 'pending':
            // Receiving message indicationg that another user request changing LED state
            // in form {"type":"pending","desiredState":"0"}
            logging(data);
            pending(data.desiredState);
            break;
        case 'temp':
            // Receiving message containting new temperature
            // in form {"type":"temp","temp":"18.554688","time":"1546524503274"}
            logging(data);
            addLastTemp(data);
            break;
        case 'accelero':
            // Receiving message containting new accelerometer values
            // in form {'action': 'accelero', 'x_acc': '93', 'y_acc': '-161', 'z_acc': '982', 'time': '1546527162590'}
            logging(data);
            getLastAcceleroData(data);
            break;
        default:
            logging("ignored: ", data);
    }
};