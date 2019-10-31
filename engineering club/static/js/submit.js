var submit = function() {
    var url = "/login/";
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value
    var params = "comment="+email+"&password="+password;
    ajax(url, params, console.log);
}
