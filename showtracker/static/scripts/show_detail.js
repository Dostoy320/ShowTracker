
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
          data[i][1] + ">" + data[i][0] + "</div></li>");
      }
      watchedStatus();
      episodeOverview();
    }
  });
});

//The old watched trigger:
//<div class=update_ep_status>O</div>

// The variable 'id' is available here, giving show id
// but I think all you need is the episode id, which you should be able to
// pull here as 'ep'
// I take that back.. This ID is for Episode model, not Us

function watchedStatus() {
  $('.rating, .empty_gray, .full_gray').on('click', function(event) {
    // Stop click event from bubbling up to .season_select click
    event.stopPropagation();

    // Assigning this to variable so I can use it in the success function
    // I'm not at all sure if this is OK, but it works.
    var current = $(this).prev();

    var empty_large = "<div class=empty_large></div>";
    var full_large = "<div class=full_large></div>";
    current.append("<div id='rating_popup'><p>Rate it!</p><div id='circles'>" + empty_large + empty_large + empty_large + empty_large + empty_large + "</div>");
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


function episodeOverview() {
  $("div[class^='watched_']").on('click', function(event) {
    event.stopPropagation();
    var current = $(this);
    if (current.children()[0]){
      current.children()[0].remove();
      current.children()[0].remove();
      $('.rating').remove();
    } else {
      $('.rating').remove()
      $('#overview').remove();
      dataString = "ep_number=" + current.attr('ep');

      $.ajax({
        url: $SCRIPT_ROOT + "/episode_overview",
        data: dataString,
        success: function(data) {
          // Variables to make up rating div string
          var empty = "<div class=empty_gray></div>";
          var full = "<div class=full_gray></div>";
          var currentRating = "";
          // Construct string of divs for rating display;
          totalFull = data[1];
          totalEmpty = 5 - totalFull
          // Add a 'full' div for each rating
          for (var i=0; i < totalFull; i++) {
            currentRating = currentRating + full;
          }
          // Add an 'empty' div to reach out to 5
          for (var i=0; i < totalEmpty; i++) {
            currentRating = currentRating + empty;
          }
          current.append("<div class='rating'>" + currentRating + "</div>")
          current.append("<div id='overview'>" + data[0] + "</div");

          // Call to re-apply click event handler;
          watchedStatus();
        }
      });
    }
  });
}

/*function watchedStatus() {
  $('.rating, .empty_gray, .full_gray').on('click', function(event) {
    // Stop click event from bubbling up to .season_select click
    event.stopPropagation();
    alert('rating system goes here!');
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
}*/