$(document).ready(function(){
    $('form#main').on('submit', function(event) {
        event.preventDefault();
        var form = $('form');
        var formdiv =  $('.form');
        $.ajax({
            url: '/',
            method: 'POST',
            dataType: 'json',
//            contentType: 'application/json',
            data: JSON.stringify(form.serializeArray()),
            timeout: 31000,
            success: function(response, textStatus){
                    if (response.is_e) {
                        var msg = $('<div class="alert alert-danger" role="alert"></div>');
                        msg.append(response.e);

                        $('.alert.alert-danger').remove();
                        formdiv.prepend(msg).fadeIn();
                    } else {
                        form.remove();

                        var msg = $('<div class="alert alert-success" role="alert"></div>');
                        msg.append("<p>Dear " + response.username + ".</p>");
                        msg.append("<p>Search result will be sent on your e-mail address " + response.email + " as soon as search finished.</p>");

                        formdiv.hide().html(msg).fadeIn();
                    }
                },
            error: function(request, errorType, errorMessage){
                    form.remove();

                    var msg = $('<div class="alert alert-danger" role="alert"></div>');
                    msg.append('Error: ' + errorType + '  with message: ' + errorMessage);

                    formdiv.html(msg).fadeIn();
                }
        });
    });
});