function firebase(str){
alert(str);
	var database=str.substr(7);
	arr=database.split(".");
	database=arr[0];

/*firebase.prototype.put=function(str){
	$.ajax({
					type : 'POST',
				url  : '/insert',
				async : true,
				cache : false
			});
		
}
*/
}