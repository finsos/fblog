function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
        }
    }
    return cookieValue;
}

var loginOuter = $('#login-outer')[0];

function userLogin() {
    var url = 'http://' + location.host + '/login/?next=' + location.pathname;
    var response = $.get(url, function(data) {
            $('#login-inter .github-login').attr('href', data);
            console.log(data)
    });
    console.log(response['responseText']);
    if (loginOuter.style.display !== 'block') {
        loginOuter.style.display = 'block';
        console.log(loginOuter.style.display);
    }
}

function userLoginCancel() {
    loginOuter.style.display = 'none';
}