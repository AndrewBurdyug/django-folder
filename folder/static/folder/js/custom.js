var csrftoken = '';

var check_http_method = function(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var send_credentials = function(auth_data){
    $.ajax({
        beforeSend: function(xhr, settings){
            if (!check_http_method(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/folder/login/",
        method: "POST",
        data: auth_data
    }).done(function(data){
        if (data.status == 'OK'){
            home_url = window.location.origin + '/folder/home/';
            window.location.replace(home_url);
        } else {
            $('#fail_login_alert').fadeIn(800);
            $('#fail_login_alert').fadeOut(2000);
        }
    });
}

var send_signup_data = function(signup_data){
    $.ajax({
        beforeSend: function(xhr, settings){
            if (!check_http_method(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/folder/signup/",
        method: "POST",
        data: signup_data
    }).done(function(data){
        if (data.status == 'OK'){
            home_url = window.location.origin + '/folder/login/';
            window.location.replace(home_url);
        } else {
            $('#fail_reason').html(data.info);
            $('#fail_signup_alert').fadeIn(800).delay(1500).fadeOut(2000);
        }
    });
}


$(function() {
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    $('#login_btn').click(function(event){
        event.preventDefault();
        send_credentials({'username': $('#username').val(),
                          'password': $('#password').val()});
    });

    $('#redirect_to_signup_btn').click(function(event){
        event.preventDefault();
        signup_url = window.location.origin + '/folder/signup/';
        window.location.replace(signup_url);
    });

    $('#signup_btn').click(function(event){
        event.preventDefault();
        send_signup_data({'username': $('#username').val(),
                          'password1': $('#password1').val(),
                          'password2': $('#password2').val(),
                          'email': $('#email').val()})
    });

    $('#redirect_to_login_btn').click(function(event){
        event.preventDefault();
        signup_url = window.location.origin + '/folder/login/';
        window.location.replace(signup_url);
    });

});
