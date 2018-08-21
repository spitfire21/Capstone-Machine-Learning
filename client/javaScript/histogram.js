
google.charts.load('current', {packages: ['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  var retData = null;
   $.ajax({
          type: "GET",
          url: "http://localhost:8080/histogram",

          contentType: "application/json;",
          dataType: "text",
	  beforeSend: function (xhr) {
        /* Authorization header */
        
        	xhr.setRequestHeader("Authorization", localStorage.getItem('token'));

    		},
          success: function(response){ajaxCallBack(response);},
          failure: function(errMsg) {
            alert(errMsg);
          }
          });



          function ajaxCallBack(retString){
      retData = retString;

      retData = JSON.parse(retData);
    }

  function drawChart() {
  arr = [['Length']];
  arr2 = [['Times', 'Months']];
  for (i = 1; i <= retData['values'].length; i++){
    arr[i] = [retData['values'][i-1]];

    arr2[i] = retData['scatter'][i-1];

  }
	console.log(arr2)
    var data = google.visualization.arrayToDataTable(
      arr);
    var data2 = google.visualization.arrayToDataTable(
      arr2);

      var options = {
   title: 'Histogram Error Graph',
   legend: { position: 'none' },
   vAxis: {
       title: 'Number of Athletes'
   },
   colors: ['black'],

   hAxis: {
     ticks: [-3,-2,-1,0,1,2,3],
     title: 'Times'

   },
   bar: { gap: 0 },
explorer: {
      actions: ['dragToZoom', 'rightClickToReset'],
      axis: 'horizontal',
      keepInBounds: true,
      maxZoomIn: 4.0
  },
   histogram: {
     bucketSize: 0.05,
     maxNumBuckets: 500,
     minValue: -1,
     maxValue: 1
   }
 };

 var options2 =  {
        title: 'Scatter plot model',

        pointSize: 10,
        hAxis: {
            title: 'Times'
        },
        vAxis: {
            title: 'Months'
        },
        dataOpacity: 0.3,
        legend: { position: 'none' },

        colors: ['#995141'],

    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
    var chart2 = new google.visualization.ScatterChart(document.getElementById('chart2_div'));
    chart.draw(data, options);
    chart2.draw(data2, options2);
  }
