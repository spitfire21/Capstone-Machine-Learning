$(document).ready(function() {



var frm = $("#loginForm");

frm.submit(function (ev) {

email = $("#email").val();
password = $("#password").val();
values = JSON.parse('{"email":0,"password":0}');
values['email'] =email;
values['password']= password;

 $.ajax({
            type: "POST",
            url: "http://localhost:8080/login",
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
	if(i == "token"){
		Materialize.toast("Login Successful!", 5000);
	localStorage.setItem('token', retString);
	localStorage.setItem('email', email);
 
	$.ajax({
		type:'post',
		data:{},
		url:'home.html',
		dataType:'html',
		success:function(response){
			console.log(response);
			$('body').html(response);
			
		}
		});
	
  		
	}
	else{

  		Materialize.toast(output, 5000);
	}
	}



}


 ev.preventDefault();
    });
});
