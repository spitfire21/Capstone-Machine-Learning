


function ScatterPlot(theTimes, theMonths, RMSE) {


  var arr = [
      ['Month', 'Times', {
          'type': 'string',
          'role': 'style'
      }, {
          id: 'i0',
          type: 'number',
          role: 'interval'
      }, {
          id: 'i1',
          type: 'number',
          role: 'interval'
      }]
  ];

  for (i = 1; i < theTimes.length + 1; i++) {
      if ((i - 1) != numberOfTimes) {
          arr[i] = [parseFloat(theMonths[i - 1]), parseFloat(theTimes[i - 1]), null, null, null];
      } else {
          add = parseFloat(theTimes[i - 1]) + RMSE;
          subtract = parseFloat(theTimes[i - 1]) - RMSE;
          arr[i] = [parseFloat(theMonths[i - 1]), parseFloat(theTimes[i - 1]), 'point {size: 6; shape-type: star; fill-color: #A52714; opacity: 0.7; }', add, subtract];

      }
  }


  var data = google.visualization.arrayToDataTable(
      arr
  );

  var options = {
      title: 'Line Plot of Times with Prediction and Errorbars',
      hAxis: {
          title: 'Months',
          minValue: 0,
          maxValue: 13
      },
      vAxis: {
          title: 'Times',
          minValue: 4,
          maxValue: 12
      },
      legend: 'none',
      pointSize: 4,
      colors: ['#995141'],
      intervals: {
          'style': 'bars',
          'color': '#D3362D',
          'barWidth': 0.07,
          'lineWidth': 1,
      },
      explorer: {
          actions: ['dragToZoom', 'rightClickToReset'],
          axis: 'vertical',
          keepInBounds: true,
          maxZoomIn: 8.0
      },

      trendlines: {
          0: {
              color: 'black',
              lineWidth: 0.5,
              opacity: 0.05,


              type: 'linear'
          }
      } // Draw a trendline for data series 0.

  };

  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

  chart.draw(data, options);
}

