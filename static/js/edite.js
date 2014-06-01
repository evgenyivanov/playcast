function NewId(){
  var today = new Date();
  st = today.getFullYear().toString()+today.getMonth().toString();
  st = st + today.getDate().toString();
  st = st + today.getDate().toString();
  st = st + today.getHours().toString();
  st = st + today.getMinutes().toString();
  st = st + today.getSeconds().toString();
  st = st + today.getMilliseconds().toString();
  return st;
}





function DeleteBackgroundImage(){

    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    $("#undo")[0].innerHTML = BodyF.innerHTML;
    $("#undostyle")[0].innerHTML = BodyF.style.cssText;
    BodyF.style.backgroundImage = "none";
    $("#dialog").dialog("close");

}

function EndUploadMusic(){

   parent.parent.$("#upload_music").dialog("close");
   parent.document.getElementById("list_music").contentDocument.location.reload(true);
}

function EndUploadImage(){
   parent.parent.$("#upload_image").dialog("close");
   parent.document.getElementById("list_img").contentDocument.location.reload(true);
}
function refresh(arg){

var myDict ={'my': $("#onlymy").prop("checked"), 'words' : $("#keywords").val()};
if(arg===0){arg = 0;}

$.get("/images_list/"+arg.toString()+'/',myDict,function(data,status){
     $("#conteiner").html(data);
  });
    }

function Readers(id){
    document.location.href = "/readers/"+id+"/";
}

function DeletePlayCast(id){
    document.location.href = '/deleteplaycast/'+id+'/';
}

function DelQuest(){

    $("#dialog").dialog("open");
}
function FrameOnLoad(){

document.body.innerHTML = parent.$("#undo")[0].innerHTML + document.body.innerHTML;
document.body.style.cssText = parent.$("#undostyle")[0].innerHTML;
}

function Undo(){
    $("#myframe")[0].contentDocument.getElementsByTagName("body")[0].innerHTML = $("#undo")[0].innerHTML;
    var css = $("#undostyle")[0].innerHTML;
    $("#myframe")[0].contentDocument.getElementsByTagName("body")[0].setAttribute("style", css);
}

function VideoSet(arg){
    $('#mybox')[0].innerHTML = arg;
   obj = $("#"+arg);
   obj.resizable();
   obj.draggable();
   obj.rotatable();

}

function AddVideo(){


url = $("#select_video_url")[0].value;
url = url.replace('http://www.youtube.com/watch?v=','');
$("#undo")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].innerHTML;
$("#undostyle")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].style.cssText;
var today = NewId();

st2= "<div><div name = 'container' class='container' onclick=";
st2=st2+'"';
st2= st2+"Select('";
st2= st2+today+"'"+');';
st2=st2+'"';
st2 = st2 +' id="'+today+'_container" style="position: absolute; z-index: 4; width : 245px; height : 185px" >';
st2 = st2 + '<iframe class="content" id = "'+today+'" width="96%" height="96%" src="http://www.youtube.com/embed/'+url+'?autoplay=1" frameborder="0" allowfullscreen="allowfullscreen" data-link="http://www.youtube.com/watch?v='+url+'"></iframe>';
st2 = st2 + '</div></div>';

BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st2 + BodyF.innerHTML;
   $("#select_video").dialog("close");
document.getElementById("myframe").contentWindow.VideoSet(today+'_container');
$("#myframe")[0].contentWindow.Select(today.toString());
}

function Put(){
    active = $('#active')[0].checked;

    obj = $('#myframe_conteiner')[0];
    w = obj.style.width;
    h = obj.style.height;
    tid = $("#object_id")[0].innerHTML;
    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    $("#wait").show();

    var MyDict = {'active':active,'tid':tid,'style':BodyF.style.cssText ,'width': w,'height':h,'title': document.getElementById("title").value,'body': $('#myframe').contents().find("body").html(),'mtitle': document.getElementById("music_title").textContent,'murl': document.getElementById("music_url").textContent ,'mauthor': document.getElementById("music_author").textContent,'mperformer': document.getElementById("music_performer").textContent,'comments': myNicEditor3.instanceById('comments_text').getContent()};


$.ajax({
  type: "POST",
  url: "/put/",
  data: MyDict,
  success: function(msg){

document.getElementById('myframe').contentWindow.Screen(msg,w,h,active);
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {

     document.body.innerHTML = XMLHttpRequest.responseText;
  }
});


    $("#wait").hide();
}

function Screen(arg,w,h,active){

    document.body.innerHTML = document.body.innerHTML +'<div id="bgr"></div>';
    obj=$("#bgr")[0];
    obj.style.width = w;
    obj.style.height = h;
    obj.style.zindex = -3000;
    obj.style.backgroundImage = document.body.style.backgroundImage;

 //////////////////////////////////////////


   html2canvas(document.body, {

       allowTaint: false,
            logging:true,
  onrendered: function(canvas) {
      document.body.appendChild(canvas);
    dataURL = canvas.toDataURL("image/png");
 obj=$(canvas);
obj.remove();



$.ajax({
  type: "POST",
  url: "/save/",
  data: {'id':arg,'imageData':dataURL},
  success: function(msg){
  if (active){
  parent.document.location.href = '/playcast/'+arg;}else{
   parent.document.location.href = '/designer/'+arg+'/';
  }

  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {

     document.body.innerHTML = XMLHttpRequest.responseText;
  }
});

}}
)}

function Publisher(){

  myframe = $("#myframe")[0].contentWindow;
  myframe.$(".ui-resizable-handle").remove();
  myframe.$(".ui-rotatable-handle").remove();
  myframe.$("#mybox")[0].innerHTML="";

    var id_playcast = Put();
}


function Preview(){
title = $("#title")[0].value;
body =  $('#myframe').contents().find("body").html();
newwindow=window.open("",title);
newdocument=newwindow.document;
newdocument.write('<head><script src="/static/js/audio.min.js"></script><script> audiojs.events.ready(function() {var as = audiojs.createAll(); });</script></head>');
BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
mystyle = BodyF.style.cssText;
obj = $('#myframe_conteiner')[0];
w = obj.style.width;
h = obj.style.height;
newdocument.write('<BODY>');
st = "<div style='"+mystyle+" width :"+w+"; height :"+h+";'>";
newdocument.write(st);

newdocument.write('<title>'+title+'</title>');
newdocument.write('<div>'+body+'</div><br />');
newdocument.write('</div>');
newdocument.write('<br /><audio  preload="auto" autoplay="true" loop="loop" src=/media/'+$("#music_url")[0].innerHTML+'  /><br />');
comment = myNicEditor3.instanceById('comments_text').getContent();
newdocument.write('<div>'+comment+'</div>');
newdocument.write('</BODY>');
newdocument.close();
}

function AddMusic(url,title,author,performer){

$("#music_url")[0].innerHTML=url;
$("#music_title")[0].innerHTML=title;
$("#music_author")[0].innerHTML=author;
$("#music_performer")[0].innerHTML=performer;
$("#select_music").dialog("close");
}

function AddImage(arg,w,h){

$("#undo")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].innerHTML;
$("#undostyle")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].style.cssText;
if ($("#type_select_image").html() === '0'){
obj= $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
obj.style.backgroundImage = 'url(' + arg + ')';

$("#dialog").dialog("close");
}

if ($("#type_select_image").html() === '1'){
var today = NewId();
st= "<div name = 'container' class='container' onclick=";
st = st + '"Select(';
st = st +"'"+today+"');"
st = st +'" onclick="Select(';
st = st +"'"+today+"');";
st = st +'" id="'+today+'_container" style="position: absolute; z-index: 7; top: 0px;  -webkit-transform:matrix(1,0,0,1,0,0);-moz-transform:matrix(1,0,0,1,0,0);-ms-transform:matrix(1,0,0,1,0,0);" />   <img  class="content" src="'+arg+'" width="50" height="50" alt="" id="'+today;
st = st +'" style=""></div>';
BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;
obj = $("#myframe")[0].contentDocument.getElementById(today.toString());
obj.width = w;
obj.height = h;
$("#select_image").dialog("close");
$("#myframe")[0].contentWindow.Select(today.toString());

}
}



function EditeMyText(){

    id = $("#text_edite_id")[0].innerHTML;
    myDiv = $("#myframe")[0].contentDocument.getElementById(id);
    myDiv.innerHTML = myNicEditor2.instanceById('text_edite_text').getContent();
    parent.$("#text_edite").dialog("close");
}

function EditeText(arg){
txt = $("#"+arg)[0].innerHTML;

parent.$("#text_edite_id")[0].innerHTML = arg;
parent.myNicEditor2.instanceById('text_edite_text').setContent(txt);
parent.$("#text_edite").dialog("open");
}

function HTML(){
bodyF = $("#myframe").contents().find("body");
alert(bodyF.html());
}

function Index(arg){
myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;

if (myItem === ''){
    return;
}
  obj = $('#myframe').contents().find('#'+myItem);
  obj_parent = obj.parent().parent()[0];
  obj_parent.style.zIndex = (parseInt(obj_parent.style.zIndex) + parseInt(arg)).toString();

}

function DeleteItem(){
myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;

if (myItem === ''){
    return;
}
  obj = $('#myframe').contents().find('#'+myItem);
  obj.parent().parent()[0].remove();

}


function AddText(){
$("#dialog_text").dialog("close");
text = myNicEditor.instanceById('my_text').getContent();

stop = true;

while (1==1){
    n = text.indexOf('<div>');

    if (n>-1){
        stop = false;
        text = text.replace("<div>","<br />");
    }


    n = text.indexOf('</div>');
    if (n>-1){
        stop = false;
        text = text.replace("</div>","");
    }


    if (stop){
        break;
    }
    stop = true;
}



var today = NewId();
st = '<div name = ';
st =st+"'container' class='container' onclick=";
st=st+'"Select(';
st =st + "'"+today+"');";
st=st+'" ondblclick= "EditeText(';
st = st + "'"+today+"');";


st=st+'" id = "'+today+'_container" style="position: absolute; z-index: 10; opacity: 1; -webkit-transform:matrix(1,0,0,1,0,0);-moz-transform:matrix(1,0,0,1,0,0); -ms-transform:matrix(1,0,0,1,0,0);" ><div><p class="content" id="'+today+'">';
st = st+text;
st = st+'</p></div></div>';


BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;
$("#myframe")[0].contentWindow.Select(today.toString());

}

function ColorBackground(){

$("#undo")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].innerHTML;
$("#undostyle")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].style.cssText;
var color = $("#selectedColor")[0].value;
obj =  $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
obj.style.backgroundColor = '#'+color;
$("#dialog").dialog("close");

}



function Clone(){

    myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;

if (myItem === ''){
    return;
}

  obj = $('#myframe').contents().find('#'+myItem);
  if (obj[0].tagName == 'IMG'){

  AddImage(obj[0].src,obj[0].width,obj[0].height);
  }


   if (obj[0].tagName == 'P'){
  var str =obj[0].innerHTML;
  var n = str.indexOf("<div");
  str =  str.substr(0, n);

  var today = NewId();
  st = '<div name = ';
  st =st+"'container' onclick=";
  st=st+'"Select(';
  st =st + "'"+today+"');";
  st=st+'" ondblclick= "EditeText(';
  st = st + "'"+today+"');";


  st=st+'" id = "'+today+'_container" style="position: absolute; z-index: 7; opacity: 1;" ><div><p id="'+today+'">';
  st = st+str;
  st = st+'</p></div></div>';

  BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
  BodyF.innerHTML = st + BodyF.innerHTML;


  }
}
////////////////////////////////////////////////////////////////////////////////

