d3.csv('https://s3.eu-west-2.amazonaws.com/bungobrew.co.uk/brewlog.csv')
  .then(makeBeerChart);

function makeBeerChart(brewlog) {
  var timeLabels = brewlog.map(function(d) {return d.TimeReading});
  var tempCData = brewlog.map(function(d) {return d.TEMP1C});
  var tempFData = brewlog.map(function(d) {return d.TEMP1F});
  
  var chart = new Chart('beer-chart', {
    type: 'line',
    data: {
      labels: timeLabels,
      datasets: [
        {
          data: tempCData,
          label: "Temp C",
          borderColor: "#3e95cd",
          fill: false
        },  
        {
          data: tempFData,
          label: "Temp F",
          borderColor: "#8e5ea2",
          fill: false
        }
      ]  
    },
    options: {
      title: {
        display: true,
        text: 'Brewing Progress'
      }
    }
  });
}