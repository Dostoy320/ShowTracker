
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
        $('#episodes').append("<li><div class=watched_" + data[i][2] + " ep=" +
          data[i][1] + ">" + data[i][0] + "</div><div class=update_ep_status>X</div></li>");
      }
      watchedStatus();
      episodeOverview();
    }
  });
});

function episodeOverview() {
  $("div[class^='watched_']").on('click', function(event) {
    event.stopPropagation();
    var current = $(this);
    if (current.children()[0]){
      current.children()[0].remove();
    } else {
      $('#overview').remove();
      dataString = "ep_number=" + current.attr('ep');

      $.ajax({
        url: $SCRIPT_ROOT + "/episode_overview",
        data: dataString,
        // You've got the show overview arriving here, so something with it.
        success: function(data) {
          current.append("<div id='overview'>" + data + "</div");
        }
      });
    }
    
  });
}

function watchedStatus() {
  $('.update_ep_status').on('click', function(event) {
    // Stop click event from bubbling up to .season_select click
    event.stopPropagation();
    // Assigning this to variable so I can use it in the success function
    // I'm not at all sure if this is OK, but it works.
    var current = $(this).prev();
    if (current.attr('class') == 'watched_true') {
      return true;
    } else {
      episode_id = current.attr('ep');
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
     }
  });
}