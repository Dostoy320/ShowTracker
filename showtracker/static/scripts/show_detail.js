
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

// Rating popup builder
function ratingPopupBuilder(rating) {

  // Get rating of current episode
  var currentRating = rating;

  // Prep string components to build rating_popup div.
  var string_rating_element = "<div id='rating_popup'><p>Rate it!</p><div id='circles'>";
  var string_div_class = "<div class=";
  var string_position = "position=";
  var string_div_end = "></div>";
  var string_element_end = "</div></div>";
  // Initialize position variable to label circle divs 1-5
  var pos_inc = 1;
  // Build rating_popup;
  for (i=0; i<5; i++) {
    //If the episode has a rating, adjust rating to match
    if (pos_inc <= currentRating) {
      type = "full_large ";
    } else {
      type = "empty_large ";
    }
    // Combine elements and increment 'position' attribute:
    string_rating_element = string_rating_element + string_div_class + type;
    string_rating_element = string_rating_element + string_position + (i + 1) +  string_div_end;
    pos_inc++;
  }
  return string_rating_element = string_rating_element + string_element_end;
}

// Receive rating from rating popup"

function getRating() {
  $('.full_large, .empty_large').on('click', function(event) {
    event.stopPropagation();
    var position = $(this).attr('position');

    // Reusing the dataString variable created by episodeOverview
    var episode_number = dataString;
    dataString = episode_number + "&ep_rating=" + position;

    $.ajax({
      url: $SCRIPT_ROOT + "/episode_rating",
      data: dataString,
      dataType: "json",
      success: function(data) {
        rating_popup = ratingPopupBuilder(data[0])
        $('#rating_popup').remove();
        $('.rating').append(rating_popup);
      }
    });
    // Resetting dataString to stop string from building on old concat
    dataString = episode_number;
    getRating();
  })
}





// Fire rating popup:
function watchedStatus() {
  $('.rating, .empty_gray, .full_gray').on('click', function(event) {
    // Stop click event from bubbling up to .season_select click
    event.stopPropagation();

    // Assigning this to variable so I can use it in the success function
    // I'm not at all sure if this is OK, but it works.
    var current = $(this).prev();

    // Get rating of current episode
    currentRating = current.parent('.rating').attr('rating');

    string_rating_element = ratingPopupBuilder(currentRating);

    current.append(string_rating_element);

    getRating();
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
          // Add an 'empty' div to build out to 5
          for (var i=0; i < totalEmpty; i++) {
            currentRating = currentRating + empty;
          }
          current.append("<div class='rating' rating='" + totalFull + "' ep='" + current.attr('ep') + "'>" + currentRating + "</div>")
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