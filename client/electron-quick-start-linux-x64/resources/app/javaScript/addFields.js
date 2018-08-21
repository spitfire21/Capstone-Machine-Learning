// This was an example that I found online and made work for our program.
function addFields(){
	
    // Number of inputs to create
    numberOfTimes = document.getElementById("member").value;
    if(numberOfTimes > 16)
    numberOfTimes = 16;

    // Container <div> where dynamic content will be placed
    var container = document.getElementById("container");
    var container2 = document.getElementById("container2");

    // Clear previous contents of the container

    for (i=0;i<numberOfTimes;i++){
        // Append a node with a random text
        container.appendChild(document.createTextNode("Time " + (i+1)));

        // Create an <input> element, set its type and name attributes
        var input = document.createElement("input");
        input.type = "number";
        input.id = "member" + i;
        input.placeholder = "10.50"
        container.appendChild(input);

        container2.appendChild(document.createTextNode("Month "+ (i+1)));
        var input = document.createElement("input");
        input.type = "text";
        input.id = "member" + (i+20);
        input.placeholder = "3/15"
        input.pattern = "[1-6]+/+[1-31]"
        container2.appendChild(input);
    }
}
