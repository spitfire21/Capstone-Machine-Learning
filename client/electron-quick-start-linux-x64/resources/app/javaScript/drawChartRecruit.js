google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawCurveTypes);
function drawCurveTypes(response) {

      var data = JSON.parse(response);
      var numberOfAthletes = data.athletes[0].length;
      var name = data.athletes[0][0];
      var len = data.times[0][0].length;
      var dataLists = [];
      for(i=0; i<numberOfAthletes; i++){
		  var numberOfSent = 0
          for(j=0; j<len; j++){
             var list = [];
             for(k=0; k<=numberOfAthletes; k++){
               list[k] = null;
             }
             if(typeof data.times[0][i][j] != 'undefined' && parseFloat(data.times[0][i][j][1]) > 0 ){
             list[0] = parseFloat(data.times[0][i][j][1]);

             numberOfSent++;
           }else{

             list[0] = null;
           }
           if(typeof data.times[0][i][j] != "undefined"){
			     list[i+1] = parseFloat(data.times[0][i][j][0]);
         }
           dataLists.push(list);
           }
           console.log("Predicted Time: " + parseFloat(data.values[i][0][0]) + "Predicted Date " + parseFloat(data.values[i][0][1]));


            x = 0;

            while (typeof data.values[i] != "undefined" && parseFloat(data.values[i][0][x]) != 0 && x < 12 && x < data.values[i][0].length ){
				check = (parseFloat(data.values[i][0][0]) - parseFloat(data.times[0][i][+numberOfSent-1][0]))
				 var t = [];

          			 for(v=0; v<=numberOfAthletes; v++){
            			 	t[v]=null;
           			}

				if (check  > -0.35 && check < 1 && parseFloat(data.values[i][0][+x+1]) > parseFloat(data.times[0][i][+numberOfSent-1][1])){
					if(x < 2 || parseFloat(data.values[i][0][+x+1]) > parseFloat(data.values[i][0][+x - 1])){
					t[0]= parseFloat(data.values[i][0][+x+1]);
           			t[+i+1]= parseFloat(data.values[i][0][+x]);
                //t[numberOfAthletes+1] =  'point {size: 18; shape-type: star;}';
					dataLists.push(t);
          console.log(t);
				}

				}
				x=x+2;


		}

    }
console.log(dataLists);


      var chartData = new google.visualization.DataTable();
      chartData.addColumn('number', 'X');
      for(i=0; i<numberOfAthletes; i++){
        chartData.addColumn('number',data.athletes[0][i]);
      }


      chartData.addRows(dataLists);

      var options = {
          title: 'Track Prediction',
          titlePosition: 'right',
          curveType: 'function',
          pointSize: 10,
          hAxis: {
              title: 'Months'
          },
          vAxis: {
              title: 'Times'
          },
          explorer: {
                actions: ['dragToZoom', 'rightClickToReset'],
                axis: 'vertical',
                keepInBounds: true,
                maxZoomIn: 4.0
            },
          dataOpacity: 0.3,
          legend: {
              position: 'right'
          }
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(chartData, options);

      var columns = [];
  var series = {};
  for (var i = 0; i < chartData.getNumberOfColumns(); i++) {
      columns.push(i);
      if (i > 0) {
          series[i - 1] = {};
      }
  }

  var options = {
    title: 'Track Prediction',
    curveType: 'function',
    pointSize: 10,
    hAxis: {
        title: 'Months'
    },
    vAxis: {
        title: 'Times'
    },
    explorer: {
          actions: ['dragToZoom', 'rightClickToReset'],
          axis: 'vertical',
          keepInBounds: true,
          maxZoomIn: 4.0
      },
    dataOpacity: 0.3,
    legend: {
        position: 'right'
    },
      series: series
  }
//http://jqfaq.com/how-to-hideshow-lines-in-line-chart/#commentarea
    google.visualization.events.addListener(chart, 'select', function () {
       var click = chart.getSelection();
       if (click.length > 0) {
           if (click[0].row === null) {
               var col = click[0].column;
               if (columns[col] == col) {
                   columns[col] = {
                       label: chartData.getColumnLabel(col),
                       type: chartData.getColumnType(col),
                       calc: function () {
                           return null;
                       }
                   };
                   series[col - 1].color = '#000000';
               }
               else {
                   columns[col] = col;
                   series[col - 1].color = null;
               }

               var newGraph = new google.visualization.DataView(chartData);
               newGraph.setColumns(columns);
               chart.draw(newGraph, options);
           }
       }
   });
}
