AWS.config.region = 'eu-west-1'; // Region
AWS.config.credentials = new AWS.Credentials('AKIAIN4AYBLH6UO5F5AA', 'LXJml7z2byIxKA5aYRvLjRee00MGm4BD3vz0BTWy');
var dynamodb = new AWS.DynamoDB();

var Name='Name';

var params = { 
                TableName: 'temp',
				KeyConditionExpression: '#Name = :Inside',
				ExpressionAttributeNames: {
                  "#Name": "Name",
                },
                ExpressionAttributeValues: {
                  ":Inside": { "S" : "Inside"}
                }
             };
             
var dataT=[];
             
dynamodb.query(params, function(err, data) {
	if (err) {
		console.log(err);
		return null;
	} else {
		for (var i in data['Items']) {
			TemperatureRead = parseFloat(data['Items'][i]['temp']['N']);
			TimeRead = parseFloat(data['Items'][i]['Time']['N']);

			var obj=[];
			obj.push(TimeRead);
			obj.push(TemperatureRead);
			dataT.push(obj);
		}
	}



	Highcharts.chart('container', {

		series: [{
			name: 'Inside',
			data: dataT
			}],
		
		title: {
			text: 'Temperature'
		},
		xAxis: {
			type: 'datetime',

		},

		yAxis: {
			title: {
				text: '°C'
			}
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'middle'
		},

		/*plotOptions: {
			series: {
				label: {
					connectorAllowed: false
				},
				pointStart: 0
			}
		},*/

		responsive: {
			rules: [{
				condition: {
					maxWidth: 500
				},
				chartOptions: {
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'bottom'
					}
				}
			}]
		}

	}); 

});


// function conditionalDelete() {
//     var temp = "21.887207";

//     var params = {
//         TableName: "temp",
//         Key:{
// 			"Name": {S: "Inside"},
// 			"Time": {N: "1544748468874"}
//         }
//     };

//     dynamodb.deleteItem(params, function(err, data) {
//         if (err) {
//             document.getElementById('textarea').innerHTML = "The conditional delete failed: " + "\n" + JSON.stringify(err, undefined, 2);
//         } else {
//             document.getElementById('textarea').innerHTML = "The conditional delete succeeded: " + "\n" + JSON.stringify(data, undefined, 2);
//         }
//     });
// }