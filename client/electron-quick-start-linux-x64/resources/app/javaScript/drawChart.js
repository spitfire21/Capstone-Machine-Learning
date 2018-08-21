function LoadGoogle()
    {
        if(typeof google != 'undefined' && google && google.load)
        {
            google.charts.load('current', {packages: ['corechart']});
           google.charts.load('visualization', {packages: ['corechart']});
			google.charts.setOnLoadCallback(drawChart);
			
			
			

        }
        else
        {
            // Retry later...
            setTimeout(LoadGoogle, 30);
        }
    }

  
     google.charts.load('visualization', {packages: ['corechart']});      
    LoadGoogle();


function drawChart(theTimes, theMonths) {
	 google.charts.load('visualization', {packages: ['corechart']});
 LoadGoogle();

var numberOfTimes = document.getElementById("member").value;
    var arr = [
        ['Month', 'Times', {
            'type': 'string',
            'role': 'style'
        }]
    ];
    for (i = 1; i < theTimes.length -1; i++) {
        if (i < +numberOfTimes + +1) {
            arr[i] = [parseFloat(theMonths[i - 1]), parseFloat(theTimes[i - 1]), null];
        } else {
            arr[i] = [parseFloat(theMonths[i - 1]), parseFloat(theTimes[i - 1]), 'point {size: 18; shape-type: star; fill-color: #A52714; }'];
        }
    }

    var data = google.visualization.arrayToDataTable(
        arr
    );

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
        dataOpacity: 0.3,
        legend: {
            position: 'right'
        },
        colors: ['#995141'],
        trendlines: {
            0: {}
        } // Draw a trendline for data series 0.
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);

}

