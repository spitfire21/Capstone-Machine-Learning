$("a").on('click', function() {
	
	$.ajax({
		type:'post',
		data:{},
		url: $(this).attr( 'href' ),
		dataType:'html',
		success:function(response){
			console.log(response);
		//$( "body" ).html( response );
		//alert(document.getElementsByTagName('head')[0].innerHtml);
			
		}
		});
	
});
