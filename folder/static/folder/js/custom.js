var csrftoken = '';
var file = '';
var ajax_extra_options = {};
var delete_url = '';

PNotify.prototype.options.styling = "fontawesome";

var check_http_method = function(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var service_ok_urls = {
    'login': '/folder/home/',
    'signup': '/folder/login/',
    'home': '/folder/home/',
    'delete': '/folder/home/',
    'delete_shared_link': '',
    'create_shared_link': ''
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
                new PNotify({
                        delay: 4000,
                        type: 'success',
                        title: 'Статус операции',
                        text: 'Файл <strong>"' + backend_response.info.name + '"</strong> успешно загружен!'
                    });

                if(backend_response.info.created == false && Object.getOwnPropertyNames(backend_response.info.owners).length != 0){
                    var file_info = 'Этот файл также есть у';
                    for(var username in backend_response.info.owners) {
                        file_info += ' <strong>' + username + '</strong> с названием <strong>"' + backend_response.info.owners[username] + '"</strong>';
                    }
                new PNotify({
                        delay: 4000,
                        type: 'info',
                        title: 'Найден Дубликат',
                        text: file_info
                    });
                }
            } else if (service_type == 'create_shared_link'){
                $('#file_shared_link_op_' + backend_response.info.file_link_id).html(
                    'Ссылка: <a href="/folder/shared/' + backend_response.info.shared_link + '"><small>' + backend_response.info.file_link_name + '</small></a><a href="#" name="' + backend_response.info.file_link_id + '" class="delete_shared_link"><i class="fa fa-trash-o fa-fw"></i></a>'
                );
            } else {
                if (service_ok_urls[service_type]) {
                    home_url = window.location.origin + service_ok_urls[service_type];
                    window.location.replace(home_url);
                }
            }
        } else {
            if (service_type == 'home') {
                new PNotify({
                        delay: 4000,
                        type: 'error',
                        title: 'Статус операции',
                        text: 'Ошибка: <strong>' + JSON.stringify(backend_response.info) + '</strong>'
                    });
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

    $('#center_upload_btn, #header_upload_btn').click(function(event){
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

    $('#upload_dialog').on('hidden.bs.modal', function(){
        location.reload();
    });

    $('.delete_file').click(function(event){
        event.preventDefault();
        var elem = $(this);
        delete_url = elem.attr('href');
        var file_name = elem.attr('name');
        $('#file_to_delete').text('Вы уверены, что хотите удалить файл "' + file_name +'" ?');
        $('#delete_dialog').modal('show');
    });

    $('#delete_file_no').click(function(event){
        event.preventDefault();
        $('#delete_dialog').modal('hide');
    });

    $('#delete_file_yes').click(function(event){
        event.preventDefault();
        $.extend(ajax_extra_options, {'url': delete_url});
        send_data('delete', {})
        ajax_extra_options = {};
    });

    $('.file_shared_link_operations').on('click', '.delete_shared_link', function(event){
        event.preventDefault();
        var elem = $(this);
        delete_url = '/folder/delete_shared_link/' + elem.attr('name');
        $.extend(ajax_extra_options, {'url': delete_url, 'method': 'GET'});
        send_data('delete_shared_link', {});
        ajax_extra_options = {};
        $('#file_shared_link_op_' + elem.attr('name')).html(
            '<a href="#" name="' + elem.attr('name') + '" class="create_shared_link"><i class="fa fa-link fa-fw"></i> Создать ссылку</a>'
        );
    });

    $('.file_shared_link_operations').on('click', '.create_shared_link', function(event){
        event.preventDefault();
        var elem = $(this);
        create_url = '/folder/create_shared_link/' + elem.attr('name');
        $.extend(ajax_extra_options, {'url': create_url, 'method': 'GET'});
        send_data('create_shared_link', {});
        ajax_extra_options = {};
    });

});
