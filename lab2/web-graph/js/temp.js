var dynamodb = new AWS.DynamoDB();

var chartTemp;

var params = { 
    TableName: 'temp',
	KeyConditionExpression: '#Name = :Inside',
	ExpressionAttributeNames: {
        "#Name": "Name",
    },
    ExpressionAttributeValues: {
        ":Inside": { "S" : "Inside"}
    },
};

function getNDataFromDynamoDB() {
    return new Promise(function (resolve, reject) {
        dynamodb.query(params, function(err, data) {
            if (err) {
                logging(err);
                return reject(err);
            } 
            let dataTemp = [];
            for (var i in data['Items']) {
                TemperatureRead = parseFloat(data['Items'][i]['temp']['N']);
                TimeRead = parseFloat(data['Items'][i]['Time']['N']);
                dataTemp.push({
                    x: TimeRead,
                    y: TemperatureRead
                })
            }
            resolve(dataTemp);
        });
    });
}

(async function() {
    try {
        let dataT = await getNDataFromDynamoDB();
        buildChart(dataT);
    } catch(err) {
        logging(err);
    }
})();

function buildChart(dataT) {
    chartTemp = Highcharts.stockChart('container', {
        time: {
            useUTC: false
        },

        title: {
            text: 'Temperature (esp32)'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '°C'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            headerFormat: '<strong>{series.name}</strong><br/>',
            pointFormat: 'Time: {point.x:%Y-%m-%d %H:%M:%S}<br/>Temperature: {point.y:.4f} °C'
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'hour',
                text: 'Last hour'
            }, {
                count: 2,
                type: 'hour',
                text: '2 hours'
            }, {
                count: 12,
                type: 'hour',
                text: '12 hours'
            }, {
                count: 24,
                type: 'hour',
                text: '24 hours'
            }, {
                count: 2,
                type: 'day',
                text: '2 days'
            }, {
                count: 1,
                type: 'month',
                text: '1 month'
            }],
            inputEnabled: false,
            selected: 0,
            buttonTheme: { // styles for the buttons
                fill: 'none',
                stroke: '#6897c4',
                'stroke-width': 1,
                width: 70,
                r: 8,
                style: {
                    color: '#6897c4',
                    fontWeight: 'bold',
                },
                states: {
                    hover: {
                    },
                    select: {
                        fill: '#6897c4',
                        style: {
                            color: 'white'
                        }
                    }
                    // disabled: { ... }
                }
            },
        },
        series: [{
            name: 'Inside',
            data: dataT
        }]
    });
}

function addLastTemp(data) {
    var x = Number(data['time']),
		y = Number(data['temp']);
	logging("Point [" + x + ", " + y + "] added");
    var series = chartTemp.series[0];
    series.addPoint([x, y], true, true);
}