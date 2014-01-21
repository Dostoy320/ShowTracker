
// List episodes for clicked season
$('.season_select').on('click', function() {

  // Clear previous results
  if ($(this).children().length > 0) {
    $('#episodes').remove();
    return 1;
  } else {
    $('#episodes').remove();
  }

  // Assigning this to variable so I can use it in the success function
  // I'm not at all sure if this is OK, but it works.
  var current = $(this);



  //var id = {{ show.id }};
  var season = $(this).attr('season');
  dataString = "id=" + id + "&season=" + season;

  $.ajax({
    url: $SCRIPT_ROOT + "/episode_detail",
    data: dataString,
    dataType: "json",
    success: function(data) {
      // List episodes with class and episode id attributes
      $(current).append("<ul id='episodes'></ul>");
      for (i in data){
        $('#episodes').append("<li class=watched_" + data[i][2] + " ep=" +
          data[i][1] + ">" + data[i][0] + "</li>");
      }
      watchedStatus();
    }
  });
});

function watchedStatus() {
  $('.watched_false').on('click', function(event) {
    // Stop click event from bubbling up to .season_select click
    event.stopPropagation();
    // Assigning this to variable so I can use it in the success function
    // I'm not at all sure if this is OK, but it works.
    current = $(this)
    episode_id = $(this).attr('ep');
    status = 'watched';
    dataString = "ep_id=" + episode_id + "&status=" + status;

    $.ajax({
      url: $SCRIPT_ROOT + "/episode_status",
      data: dataString,
      dataType: "json",
      success: function() {
        current.attr('class', 'watched_true');
      }
    });
  });
}