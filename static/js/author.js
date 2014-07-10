$(function(){
        var theDialog = $("#dialog").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '100',
            height:'800',
        });
})

function SendPresent(){
         $("#dialog").dialog("open");
}

function Account(){
        document.location.href='/account';
}

$(document).ready(function (){
$('.collection').on('click',function(){
var a = document.createElement('a');
a.href=$(this).attr('data-href');
document.body.appendChild(a);
a.click();
});
});