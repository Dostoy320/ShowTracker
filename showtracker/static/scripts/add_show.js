// Some indication that something is actually happening when you submit a show.

$('#show_submit').on('submit', function() {
	$(this).append('<p>Loading Show Data...</p>');
});