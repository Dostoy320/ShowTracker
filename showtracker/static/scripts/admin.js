$('#shows li').on('click', function() {
	$(this).append("<div class='del_confirm'>Are you sure about this?</div>");
});



//<a href="{{ url_for('admin') }}?action=delete&value={{ show.id }}">