var csrftoken = '';

var check_http_method = function(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var service_ok_urls = {
    'login': '/folder/home/',
    'signup': '/folder/login/'
}

var format_error_msg = function(data){
    var formated_errors = '<dl class="dl-horizontal">';
    $.each(data, function(key, value){
        formated_errors += '<dt>' + key + '</dt>';
        formated_errors += '<dd>' + value + '</dd>';
    });
    formated_errors += '</dl>';
    return formated_errors;
}


var send_data = function(service_type, data){
    $.ajax({
        beforeSend: function(xhr, settings){
            if (!check_http_method(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/folder/" + service_type + "/",
        method: "POST",
        data: data
    }).done(function(backend_response){
        if (backend_response.status == 'OK'){
            home_url = window.location.origin + service_ok_urls[service_type];
            window.location.replace(home_url);
        } else {
            $('#fail_reason').html(format_error_msg(backend_response.info));
            $('#fail_' + service_type + '_alert').fadeIn(800).delay(1500).fadeOut(2000);
        }
    });
}

$(function() {
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    $('#login_btn').click(function(event){
        event.preventDefault();
        send_data('login', {'username': $('#username').val(),
                            'password': $('#password').val()});
    });

    $('#redirect_to_signup_btn').click(function(event){
        event.preventDefault();
        signup_url = window.location.origin + '/folder/signup/';
        window.location.replace(signup_url);
    });

    $('#signup_btn').click(function(event){
        event.preventDefault();
        send_data('signup', {'username': $('#username').val(),
                             'password1': $('#password1').val(),
                             'password2': $('#password2').val(),
                             'email': $('#email').val()});
    });

    $('#redirect_to_login_btn').click(function(event){
        event.preventDefault();
        signup_url = window.location.origin + '/folder/login/';
        window.location.replace(signup_url);
    });

});
