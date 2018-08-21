	//http://wabism.com/html5-file-api-how-to-upload-files-dynamically-using-ajax/
function loadFile() {
	// Retrieve the FileList object from the referenced element ID
	var myFileList = document.getElementById('upload_file').files;

	// Grab the first File Object from the FileList
	var myFile = myFileList[0];

	// Set some variables containing the three attributes of the file
	var myFileName = myFile.name;
	var myFileSize = myFile.size;
	var myFileType = myFile.type;

	// Alert the information we just gathered
	//alert("FileName: " + myFileName + "- FileSize: " + myFileSize + " - FileType: " + myFileType);

	// Let's upload the complete file object
	uploadFile(myFile);
}
