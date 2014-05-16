function EditeProfile(){
    $("#editprofile")[0].src = $("#editprofile")[0].src;
    $("#dialog").dialog("open");
    }

function LogIn(){
l = $("#login")[0].value;
p = $("#password")[0].value;

$.get( "/mylogin",{'login':l,'password':p}, function( data ) {
  $( ".result" ).html( data );

  $("#auth")[0].innerHTML = data;
});
}

function logout(){
    document.location.href="/admin/logout/?next=/";
}