$(function(){
        var theDialog = $("#dialog").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '1000',
            height:'700',
        });


            var theDialog2 = $("#dialog_text").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '800',
            height:'330',
        });

           var theDialog3 = $("#text_edite").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '800',
            height:'330',
        });


         var theDialog4 = $("#select_image").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '960',
            height:'380',
        });


          var theDialog5 = $("#upload_image").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '420',
            height:'290',
        });


  var theDialog6 = $("#select_music").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '960',
            height:'580',
        });


          var theDialog7 = $("#upload_music").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '560',
            height:'380',
        });


         var theDialog8 = $("#comments").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '560',
            height:'510',
        });

        var theDialog9 = $("#select_video").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '960',
            height:'580',
        });


        var theDialog10 = $("#matrix").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '610',
            height:'100',
        });

         var theDialog11 = $("#opacity").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '250',
            height:'300',
        });


         var theDialog12 = $("#border").dialog({
            autoOpen: false,
            resizable: false,
            modal: true,
            width: '300',
            height:'300',
        });

        $("#wait").hide();


        $('#myframe_conteiner')
    .resizable({
        stop: function(e, ui) {

            BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
            BodyF.width = ui.size['width'];
            BodyF.height = ui.size['height'];
            }
    });

 window.undo = $("#undo")[0].innerHTML;
 window.undo1 = "";
 window.undo2 = "";
 window.undo3 = "";
 window.undo4 = "";
 window.undo5 = "";
 window.undo6 = "";
 window.undo7 = "";

 window.undostyle = $("#undostyle")[0].innerHTML;
 window.undostyle1 = "";
 window.undostyle2 = "";
 window.undostyle3 = "";
 window.undostyle4 = "";
 window.undostyle5 = "";
 window.undostyle6 = "";
 window.undostyle7 = "";


});


function Background_(){
    $("#type_select_image").html(0);
    $("#list_img2")[0].src= $("#list_img2")[0].src;
    $("#dialog").dialog("open")
}


function Images_(){
    $("#type_select_image").html(1);
    $("#select_image").dialog("open");
}

function Text_(){
    $("#dialog_text").dialog("open");
}

function Music_(){
    $("#select_music").dialog("open");
}

function Video_(){
    $("#select_video").dialog("open");
}

function Comm_(){
    $("#comments").dialog("open");
}

function UpImg_(){
    document.getElementById("upload2").contentDocument.location.reload(true);
    $("#upload_image").dialog("open");
}

function UpImgClose_(){
    $("#select_image").dialog("close");
}

function UpImgClose2_(){
    $("#upload_image").dialog("close");
    document.getElementById("list_img").contentDocument.location.reload(true);
}

function UpMusic_(){
    $("#upload_music").dialog("open");
}

function UpMusicClose_(){
     $("#select_music").dialog("close");
}