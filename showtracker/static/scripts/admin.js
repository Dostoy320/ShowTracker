$("#delete_user").on('click', function() {
	$("#confirm_popup").css("display", "block");

	$(".confirm_button").on("click", function() {
		if ($(this).attr("value") == 'yes') {
			window.location = "admin?action=delete_user";
		} else {
			$("#confirm_popup").css("display", "none");
		}
	});
})