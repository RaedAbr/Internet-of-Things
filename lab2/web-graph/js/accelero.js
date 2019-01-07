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
var acceleroData;
var acceleroFirstTime = true;

const loaderDivAccelero = document.getElementById("loader-div-accelero");
const container2 = document.getElementById("container2");

function getLastAcceleroData(data) { 
    if (acceleroFirstTime) {
        loaderDivAccelero.hidden = true;
        container2.style.display = "block";
    }
    X_acc = Number(data['x_acc']);
    Y_acc = Number(data['y_acc']);
    Z_acc = Number(data['z_acc']);
    time = Number(data['time']);
    
    acceleroData = {x_acc: X_acc, y_acc: Y_acc, z_acc: Z_acc};

    // add data in the textarea
    var options = {
        year: "numeric", month: "numeric", day: "numeric",
        hour: "numeric", minute: "numeric", second: "numeric", hour12: false};
    var dateTime = new Date(time);
    var dateTimeString = new Intl.DateTimeFormat("en-US", options).format(dateTime);
    var textarea = document.getElementById("textarea");
    textarea.value += "** " + dateTimeString + " **\n" + 
        JSON.stringify(acceleroData) + "\n\n";
    textarea.scrollTop = textarea.scrollHeight;

    // update data in the 3D chart
    chart.series[0].setData([[X_acc, Y_acc, Z_acc]], true);
}

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