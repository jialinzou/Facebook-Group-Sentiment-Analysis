$( document ).ready(function()
{
    $( "#compute" ).click(function()
    {
        // Remove all the html inside of the div
        $("#compute_results").empty();

        // Create an url with the number of sample and facebook group name
        var url = window.location.href+
                    "train?num_samples="+$("#num_samples").val()+
                    "&facebook_group="+$("#facebook_group_name").val();

        // Fire off an AJAX get request
        $.get(url, function( data )
        {
            var html_start = "<div class=\"ui segment\">\
                                  <table class=\"ui celled table\"> \
                                      <thead> \
                                          <tr> \
                                              <th>User</th>\
                                              <th>User ID</th>\
                                              <th>Sentiment</th>\
                                          </tr>\
                                      </thead>\
                                      <tbody>";

            var html_mid = "";

            var html_end = "          </tbody>\
                                  </table>\
                              </div>";

            if (data.user_sentiment)
            {
                for (var i = 0; i < data.user_sentiment.length; i++) {
                    html_mid += "<tr>";
                    html_mid += "<td>" + data.user_sentiment[i].username + "</td>";
                    html_mid += "<td>" + data.user_sentiment[i].user_id + "</td>";
                    html_mid += "<td>" + data.user_sentiment[i].mean_predicted_sentiment + "</td>";
                    html_mid += "<tr>";
                }
            }

            $("#compute_results").append(html_start+html_mid+html_end);

            var html_start = "<div class=\"ui segment\">\
                                  <table class=\"ui celled table\"> \
                                      <thead> \
                                          <tr> \
                                              <th>Status</th>\
                                              <th>Message</th>\
                                          </tr>\
                                      </thead>\
                                      <tbody>";

            var html_mid = "";

            var html_end = "          </tbody>\
                                  </table>\
                              </div>";

            html_mid += "<tr>";
            html_mid += "<td>status</td>";
            html_mid += "<td>" + data.status + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>message</td>";
            html_mid += "<td>" + data.message + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>yelp_message</td>";
            html_mid += "<td>" + data.yelp_message + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>yelp_exception</td>";
            html_mid += "<td>" + data.yelp_exception + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>yelp_count</td>";
            html_mid += "<td>" + data.yelp_count + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>facebook_message</td>";
            html_mid += "<td>" + data.facebook_message + "</td>";
            html_mid += "<tr>";

            html_mid += "<tr>";
            html_mid += "<td>facebook_count</td>";
            html_mid += "<td>" + data.facebook_count + "</td>";
            html_mid += "<tr>";

            $("#compute_results").append(html_start+html_mid+html_end);
        });
    });
});