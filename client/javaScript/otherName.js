function othername() {

          var theTimes = [];
          var theMonths = [];
          var values = JSON.parse('{"values":[]}');
          for (i = 0; i < numberOfTimes; i++) {
            theTimes[i] = document.getElementById("member" + i).value;
          }
          for (i = numberOfTimes; i < 16; i++) {
            theTimes[i] = null;
          }
          var x;
          for (i = 0; i < numberOfTimes; i++) {
            x = document.getElementById("member" + (i + 20)).value;
            x = dateConvert(x);

            theMonths[i] = x
          }
          for (i = numberOfTimes; i < 16 + 20; i++) {
            theMonths[i] = null;
          }

          for (i = 0; i < numberOfTimes; i++) {
            values['values'].push([theTimes[i], theMonths[i]]);
          }
          var data;
          $.ajax({
            type: "POST",
            url: "http://localhost:8080/model/predict",
            data: JSON.stringify(values),
            contentType: "application/json;",
            dataType: "text",
	    beforeSend: function (xhr) {
        	/* Authorization header */
        	xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
       		
    		},
            success: function(response) {
                ajaxCallBack(response);
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
          });

          function ajaxCallBack(retString) {
            data = retString;

            data = JSON.parse(data);
            RMSE = data['RMSE'];
            i = 0;
            j= 0;
            while (parseFloat(data['values'][0][0][i]) != 0 && i < 16 && j < data['values'][0][0].length ){
				check = (parseFloat(theTimes[+numberOfTimes - 1]) - parseFloat(data['values'][0][0][+j]));

				if (check  > -0.35 && check < 1 && parseFloat(theMonths[+numberOfTimes - 1]) < parseFloat(data['values'][0][0][+j + 1])){

					if(j < 2 || (parseFloat(data['values'][0][0][+j + 1]) > parseFloat(data['values'][0][0][+j - 1]) && 
					
					parseFloat(data['values'][0][0][+j + 1]) <= parseFloat(theMonths[+numberOfTimes - 1])+1.0)){
					theTimes[+numberOfTimes + +i] = parseFloat(data['values'][0][0][+j]).toFixed(2);
					theMonths[+numberOfTimes + +i] = parseFloat(data['values'][0][0][+j+1]).toFixed(3);

					i++;
				}
			}
				j += 2;


		}
            //graph(theTimes, theMonths);
            
            drawChart(theTimes, theMonths);
            //ScatterPlot(theTimes, theMonths, RMSE);
          }
          }
