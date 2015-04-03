var csrftoken = '';
var file = '';
var ajax_extra_options = {};
var pnotify_options =  {
    delay: 2000,
    stack: {"dir1": "down", "dir2": "right", "push": "top"}
}

PNotify.prototype.options.styling = "fontawesome";

var check_http_method = function(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var service_ok_urls = {
    'login': '/folder/home/',
    'signup': '/folder/login/',
    'home': '/folder/home/'
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
    var options = {
        beforeSend: function(xhr, settings){
            if (!check_http_method(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/folder/" + service_type + "/",
        method: "POST",
        data: data
    };

    if (Object.getOwnPropertyNames(ajax_extra_options).length != 0){
        $.extend(options, ajax_extra_options);
    }

    $.ajax(options).done(function(backend_response){
        if (backend_response.status == 'OK'){
            if (service_type == 'home') {
                new PNotify(
                    $.extend({
                        type: 'success',
                        title: 'Статус операции',
                        text: 'Файл <strong>' + backend_response.info.name + '</strong> успешно загружен!'
                    }, pnotify_options)
                );
            } else {
                home_url = window.location.origin + service_ok_urls[service_type];
                window.location.replace(home_url);
            }
        } else {
            if (service_type == 'home') {
                new PNotify(
                    $.extend({
                        type: 'error',
                        title: 'Статус операции',
                        text: 'Ошибка: <strong>' + JSON.stringify(backend_response.info) + '</strong>'
                    }, pnotify_options)
                );
            } else {
                $('#fail_reason').html(format_error_msg(backend_response.info));
                $('#fail_' + service_type + '_alert').fadeIn(800).delay(1500).fadeOut(2000);
            }
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

    $('#center_upload_btn').click(function(event){
        event.preventDefault();
        $('#upload_dialog').modal('show');
    });

    $('#upload_cancel_btn').click(function(event){
        event.preventDefault();
        $('#upload_dialog').modal('hide');
    });

    $('#upload_send_file').click(function(event){
        event.preventDefault();
        $.extend(ajax_extra_options, {'contentType': false, 'processData': false});
        formData = new FormData();
        formData.append('data', file);
        send_data('home', formData);
        ajax_extra_options = {};
    });

    $('#id_data').change(function(event) {
        file = event.target.files[0];
    });
});
