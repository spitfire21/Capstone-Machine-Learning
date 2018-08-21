$(document).ready(function() {



var frm = $("#signUpForm");


frm.submit(function (ev) {

email = $("#email").val();
password = $("#password").val();
phone = $("#phone").val();
values = JSON.parse('{"email":0,"password":0}');
values['email'] =email;
values['password']= password;
values['phone']= phone;

 $.ajax({
            type: "POST",
            url: "http://localhost:8080/signup",
            data: JSON.stringify(values),
            contentType: "application/json;",
            dataType: "text",

            success: function(response) {
                ajaxCallBack(response);
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
          });



      function ajaxCallBack(retString){
      retData = retString;

      retData = JSON.parse(retData);

      output = "";
      for (i in retData){
	output+=i +":"+retData[i]+"\n";
	if(i == "Message"){
	$('#modal1').openModal({
      		dismissible: false, // Modal can be dismissed by clicking outside of the modal
      		opacity: 0.5, // Opacity of modal background
      		in_duration: 300, // Transition in duration
      		out_duration: 200, // Transition out duration
      		ready: function() {  }, // Callback for Modal open
      		complete: function() { return false;} // Callback for Modal close
    		}
  		);
	}
	else{

  		Materialize.toast(output, 5000);
	}
	}



}


 ev.preventDefault();
    });
    
    

});

function code_click(){
		values['code'] = $("#code").val();
		$.ajax({
            type: "POST",
            url: "http://localhost:8080/validate",
            data: JSON.stringify(values),
            contentType: "application/json;",
            dataType: "text",

            success: function(response) {
                ajaxCallBack(response);
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
          });
          
          function ajaxCallBack(retString){
			retData = retString;

			retData = JSON.parse(retData);

			output = "";
			for (i in retData){
				output+=i +":"+retData[i]+"\n";
			if(i == "Message"){
					$('#modal1').closeModal();
				// load login page
			}
			else {
				Materialize.toast(output, 5000);
			}
		
		
		
		
	}
}

}
