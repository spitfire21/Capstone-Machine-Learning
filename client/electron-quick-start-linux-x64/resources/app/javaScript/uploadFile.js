	//http://wabism.com/html5-file-api-how-to-upload-files-dynamically-using-ajax/
function uploadFile(myFileObject) {

	// Open Our formData Object
	var formData = new FormData();

	// Append our file to the formData object
	// Notice the first argument "file" and keep it in mind
	formData.append('uploaded_file', myFileObject);

	// Create our XMLHttpRequest Object
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {

		if (this.readyState == 4 && this.status == 200) {
		 console.log(xhr.response);
		 drawCurveTypes(xhr.response);
		}
	};
	
       	
       		
    		
	// Open our connection using the POST method
	xhr.open("POST", 'http://localhost:8080/upload');
	xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
	// Send the file
	xhr.send(formData);


}
