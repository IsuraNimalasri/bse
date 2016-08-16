$(document).ready(function(){
    // Variable to store your files
    var files;

    // Add events
    $('input[type=file]').on('change', function (event) {
        files = event.target.files;
    });

    $('form').on('submit', function(event) {
        event.stopPropagation(); // Stop stuff happening
        event.preventDefault(); // Totally stop stuff happening

        // Create a formdata object and add the files
        var data = new FormData();
        $.each(files, function(key, value)
        {
            data.append('book', value);
        });

        data.append('cmd', $(this).find('input[hidden=hidden]').val());

        var response_div = $(this).parent().parent().find('.container')
//        console.log($(this).parent().parent().find('.container'));

        $.ajax({
            url: '/admin',
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false, // Don't process the files
            contentType: false, // Set content type to false as jQuery will tell the server its a query string request
            success: function(data, textStatus, jqXHR) {
                    if(typeof data['error'] === 'undefined') {

                        // console.log('data: ' + JSON.stringify(data));

                        var msg = $('<div class="alert alert-success" role="alert"></div>');
                        msg.append("<p>" + JSON.stringify(data) + "</p>");

                        response_div.html(msg).fadeIn();
                    } else {
                        // Handle errors here
                        console.log('ERRORS: ' + data.error);

                        var msg = $('<div class="alert alert-danger" role="alert"></div>');
                        msg.append("<p>" + 'ERRORS: ' + data.error + "</p>");

                        response_div.html(msg).fadeIn();
                    }
                },
            error: function(jqXHR, textStatus, errorThrown) {
                    // Handle errors here
                    console.log('ERRORS: ' + textStatus);
                    // STOP LOADING SPINNER
                }
        });
    });
});