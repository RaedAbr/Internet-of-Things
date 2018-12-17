AWS.config.region = 'eu-west-1'; // Region
AWS.config.credentials = new AWS.Credentials('AKIAJDE4S4WPFLZGYAEQ', 'hCWEvI5YAvlc9ECEJTOVLt7UYRkQPDduh8jT+72R');
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
			console.log(data['Items'][i]);
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

})
