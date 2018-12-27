
var params = { 
    TableName: 'accelero',
    KeyConditionExpression: "dev_id = :dev_id",
    ExpressionAttributeValues: {
        ":dev_id": {"S": "waspmote_0"}
    },
    Limit: 1,
    ScanIndexForward: false // to reverse order and get the last record
 };

var acceleroData = {x_acc:"", y_acc:"", z_acc:""};
function getLastAcceleroData() { 
    dynamodb.query(params, function(err, data) {
        if (err) {
            console.log(err);
            return null;
        } else {
            for (var i in data['Items']) {
                X_acc = parseInt(data['Items'][i]['x_acc']['N']);
                Y_acc = parseInt(data['Items'][i]['y_acc']['N']);
                Z_acc = parseInt(data['Items'][i]['z_acc']['N']);
                if (
                    acceleroData.x_acc !== X_acc ||
                    acceleroData.y_acc !== Y_acc ||
                    acceleroData.z_acc !== Z_acc
                ) {
                    acceleroData = {x_acc: X_acc, y_acc: Y_acc, z_acc: Z_acc};

                    // add data in the textarea
                    var options = {
                        year: "numeric", month: "numeric", day: "numeric",
                        hour: "numeric", minute: "numeric", second: "numeric", hour12: false};
                    var dateTime = new Date(parseInt(data['Items'][i]['Time']['N']));
                    var dateTimeString = new Intl.DateTimeFormat("en-US", options).format(dateTime);
                    var textarea = document.getElementById("textarea");
                    textarea.value += "** " + dateTimeString + " **\n" + 
                        JSON.stringify(acceleroData) + "\n\n";
                    textarea.scrollTop = textarea.scrollHeight;

                    // update data in the 3D chart
                    chart.series[0].setData([[X_acc, Y_acc, Z_acc]], true);
                }
            }
        }
    });
}

// Give the points a 3D feel by adding a radial gradient
Highcharts.setOptions({
    colors: Highcharts.getOptions().colors.map(function (color) {
        return {
            radialGradient: {
                cx: 0.4,
                cy: 0.3,
                r: 0.5
            },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.2).get('rgb')]
            ]
        };
    })
});

var chartContent = {
    chart: {
        renderTo: 'container2',
        margin: 100,
        type: 'scatter3d',
        animation: false,
        options3d: {
            enabled: true,
            alpha: 10,
            beta: 30,
            depth: 200,
            viewDistance: 100,
            fitToPlot: false,
            frame: {
                bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
                back: { size: 1, color: 'rgba(0,0,0,0.04)' },
                side: { size: 1, color: 'rgba(0,0,0,0.06)' }
            }
        }
    },
    title: {
        text: 'Accelerometer (waspmote)'
    },
    subtitle: {
        text: 'Click and drag the plot area to rotate in space'
    },
    plotOptions: {
        scatter: {
            width: 10,
            height: 10,
            depth: 10
        }
    },
    yAxis: {
        min: -2048,
        max: 2048,
        title: {
        	text: "y_acc"
        }
    },
    xAxis: {
        min: -2048,
        max: 2048,
        title: {
        	text: "x_acc"
        }
    },
    zAxis: {
        min: -2048,
        max: 2048,
        showFirstLabel: false,
        title: {
        	text: "z_acc"
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Accelerometer',
        colorByPoint: true,
        data: []
    }]
};
// Set up the chart
var chart = new Highcharts.Chart(chartContent);

// Get and load the first accelerometer values
getLastAcceleroData();
// get and load accelerometer values each 5 seconds
setInterval(getLastAcceleroData, 5000);

// Add mouse and touch events for rotation
(function (H) {
    function dragStart(eStart) {
        eStart = chart.pointer.normalize(eStart);

        var posX = eStart.chartX,
            posY = eStart.chartY,
            alpha = chart.options.chart.options3d.alpha,
            beta = chart.options.chart.options3d.beta,
            sensitivity = 5,  // lower is more sensitive
            handlers = [];

        function drag(e) {
            // Get e.chartX and e.chartY
            e = chart.pointer.normalize(e);

            chart.update({
                chart: {
                    options3d: {
                        alpha: alpha + (e.chartY - posY) / sensitivity,
                        beta: beta + (posX - e.chartX) / sensitivity
                    }
                }
            }, undefined, undefined, false);
        }

        function unbindAll() {
            handlers.forEach(function (unbind) {
                if (unbind) {
                    unbind();
                }
            });
            handlers.length = 0;
        }

        handlers.push(H.addEvent(document, 'mousemove', drag));
        handlers.push(H.addEvent(document, 'touchmove', drag));


        handlers.push(H.addEvent(document, 'mouseup', unbindAll));
        handlers.push(H.addEvent(document, 'touchend', unbindAll));
    }
    H.addEvent(chart.container, 'mousedown', dragStart);
    H.addEvent(chart.container, 'touchstart', dragStart);
}(Highcharts));