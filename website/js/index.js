
fetchAndPlotData()

function onPageStartup()
{
	console.log("Entering in fetch");
	setInterval(fetchAndPlotData, 2000);
	console.log("Entering in fetch");
}

function fetchAndPlotData()
{
	console.log("Entering in fetch");
	fetch("/resources/data.csv")
		.then(function (response) {
			return response.text();
		})
		.then(function (text) {
			parseData(text);
			renderChart();
		})
		.catch(function (error) {
			console.log(error);
		});
}

var timestamp_data = [];
var temp_data = [];
var humi_data = [];

function parseData(text) {
	let dataAsJson = csv_to_json(text);
	temp_data = [];
	humi_data = [];
	timestamp_data = [];
	for (let entry of dataAsJson) {
		timestamp_data.push(entry.timestamp);
		temp_data.push(entry.temperature);
		humi_data.push(entry.humidity);

		//console.log(entry);
	}

	
}

function renderChart()
{
	var ctx_temp = document.getElementById('chartTemperatura');
	var ctx_humi = document.getElementById('chartUmiditate');
	console.log("ASD");
	var context = ctx_temp.getContext('2d');

	context.clearRect(0, 0, context.width, context.height);
	context = ctx_temp.getContext('2d');
	context.clearRect(0, 0, context.width, context.height);


	new Chart(ctx_temp, {
	  type: "line",
	  data: {
		labels: timestamp_data,
		datasets: [{ 
		  data: temp_data,
		  borderColor: "red",
		  fill: false
		}]
	  },
	  options: {
		legend: {display: false},
		animation: {duration: 0},
		scales: {
			yAxes: [{
				display: true,
				ticks: {
					suggestedMin: 20,
					suggestedMax: 35
				}
			}]
		}
	  }
	});

	//ctx = document.getElementById('');

	new Chart(ctx_humi, {
	  type: "line",
	  data: {
		labels: timestamp_data,
		datasets: [{ 
		  data: humi_data,
		  borderColor: "blue",
		  fill: false
		}]
	  },
	  options: {
		legend: {display: false},
		animation: {duration: 0},
		scales: {
			yAxes: [{
				display: true,
				ticks: {
					suggestedMin: 25,
					suggestedMax: 50
				}
			}]
		}
	  }
	});
}

function csv_to_json(csv){

	var lines=csv.split("\n");
  
	var result = [];
	var headers=lines[0].split(",");
  
  var index = 1;
  if (lines.length > 50)
  {
    index = lines.length - 50;
  }
	for(var i=index;i<lines.length -1;i++){
  
		var obj = {};
		var currentline=lines[i].split(",");
  
		for(var j=0;j<headers.length;j++){
			obj[headers[j]] = currentline[j];
		}
		result.push(obj);
	}
  
	return result; //JavaScript object
	//return JSON.stringify(result); //JSON
}
