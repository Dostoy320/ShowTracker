
// List episodes for clicked season
$('.season_select').on('click', function() {

  // Clear previous results
  $('#ep_list').html("");

  //var id = {{ show.id }};
  var season = $(this).attr('season');
  dataString = "id=" + id + "&season=" + season;

  $.ajax({
    url: $SCRIPT_ROOT + "/episode_detail",
    data: dataString,
    dataType: "json",
    success: function(data) {
      // List episodes with class and episode id attributes
      for (i in data){
        $('#ep_list').append("<li class=watched_" + data[i][2] + " ep=" +
          data[i][1] + ">" + data[i][0] + "</li>");
      }
      watchedStatus();
    }
  });
});

function watchedStatus() {
  $('.watched_false').on('click', function() {
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