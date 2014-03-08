// $('#del_shows li').on('click', function() {
// 	var conf = confirm("Delete forever and ever?");
// 	if (conf == true) {
// 		var dataString = "action=delete_show&id=" + this.id;
// 		$.ajax({
//     url: $SCRIPT_ROOT + "/admin",
//     data: dataString,
//     dataType: "json",
//     success: function() {
//       alert("it is done");
//     	}	
//  	 });
// 	}
// });



//<a href="{{ url_for('admin') }}?action=delete&value={{ show.id }}">