function BorderColorSelect() {

myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
obj.style.borderColor = "#"+$("#selectedColor2")[0].value;

}

function BorderRadiusSelect() {

myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
slider = $("#border_radius")[0];
obj.style.borderRadius = slider.value+"px";
label = $("#border_radius_label")[0];
label.innerHTML = slider.value.toString()+" px";
}



function BorderSelect() {

myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
slider = $("#border_value")[0];

if (obj.style.borderWidth == "0"){
obj.style.borderStyle = "";}else{
   obj.style.borderStyle = "solid";
}

obj.style.borderWidth = slider.value+"px";

label = $("#border_label")[0];
label.innerHTML = slider.value.toString()+" px";
}

function Border(){
myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];

if (obj.style.borderWidth.toString() == ''){
   obj.style.borderWidth = 0;
}
slider = $("#border_value")[0];
slider.value = parseFloat(obj.style.borderWidth);
label = $("#border_label")[0];
label.innerHTML = slider.value.toString()+"px";

slider = $("#border_radius")[0];
if (obj.style.borderRadius.toString()==""){
   slider.value = 0;
   label = $("#border_radius")[0];
   label.innerHTML = "0px";
}else{
slider.value = parseFloat(obj.style.borderRadius);
label = $("#border_radius")[0];
label.innerHTML = slider.value.toString()+"px";}

$("#border").dialog("open");
}

function BrightnessSelect() {
 myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
slider = $("#brightness_value")[0];
obj.style.webkitFilter = "brightness("+slider.value.toString()+"%)";
label = $("#brightness_label")[0];
label.innerHTML = slider.value.toString()+" %";
}

function ContrastSelect() {
 myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
slider = $("#contrast_value")[0];
obj.style.webkitFilter = "contrast("+slider.value.toString()+"%)";
label = $("#contrast_label")[0];
label.innerHTML = slider.value.toString()+" %";
}

function OpacitySelect() {
 myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];
slider = $("#opacity_value")[0];
obj.style.opacity = slider.value/100;
label = $("#opacity_label")[0];
label.innerHTML = slider.value.toString()+" %";
}

function Opacity(){

myframe = $("#myframe")[0].contentWindow;
id = myframe.$("#mybox")[0].innerHTML;
obj = myframe.$("#"+id)[0];

if (obj.style.opacity.toString() == ''){
   obj.style.opacity = 1.00;
}
slider = $("#opacity_value")[0];
slider.value = parseFloat(obj.style.opacity)*100;
label = $("#opacity_label")[0];
label.innerHTML = slider.value.toString()+" %";
$("#opacity").dialog("open");
}


function MaxZindex() {
    result = 4;
    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    collection = $(BodyF).find(".container");
    len = parseInt(collection.length);
    for (var i = 0; i < len; i++) {
    z =parseInt(collection[i].style.zIndex);

    if (result < z){
        result = z;
    }

}

    return (result+1).toString();
}

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


function uploadmusicClose(){
$("#upload_music").dialog("close");
document.getElementById("list_music").contentDocument.location.reload(true);
$("#upload_music")[0].innerHTML='<iframe  id="upload3" src="/upload_music" width="450" height="280"></iframe>';
$("#upload_music")[0].innerHTML = $("#upload_music")[0].innerHTML + '<button style="font-size: 12px; position: relative; left:350px;" onclick="uploadmusicClose();">Закрыть</button>';
}


function DeleteBackgroundImage(){

    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    To_undo_conteiner();
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

    $("#myframe")[0].contentDocument.getElementsByTagName("body")[0].innerHTML = window.undo;
    window.undo = window.undo1;
    window.undo1 = window.undo2;
    window.undo2 = window.undo3;
    window.undo3 = window.undo4;
    window.undo4 = window.undo5;
    window.undo5 = window.undo6;
    window.undo6 = window.undo7;


    $("#myframe")[0].contentDocument.getElementsByTagName("body")[0].setAttribute("style", window.undostyle);
    window.undostyle =   window.undostyle1;
    window.undostyle1    =  window.undostyle2;
    window.undostyle2 =  window.undostyle3;
    window.undostyle3 =  window.undostyle4;
    window.undostyle4 =  window.undostyle5;
    window.undostyle5 =  window.undostyle6;
    window.undostyle6 =  window.undostyle7;


    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    id = $(BodyF).find("#mybox")[0].innerHTML;
    $(BodyF).find("#mybox")[0].innerHTML="XXX";
    $("#myframe")[0].contentWindow.Select(id);
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
To_undo_conteiner();
var today = NewId();

st2= "<div><div name = 'container' class='container' onclick=";
st2=st2+'"';
st2= st2+"Select('";
st2= st2+today+"'"+');';
st2=st2+'"';
st2 = st2 +' id="'+today+'_container" style="position: absolute; z-index: 4; width : 245px; height : 185px;" >';
st2 = st2 + '<iframe class="content" id = "'+today+'" width="96%" height="96%" src="http://www.youtube.com/embed/'+url+'?autoplay=1" frameborder="0" allowfullscreen="allowfullscreen" data-link="http://www.youtube.com/watch?v='+url+'"></iframe>';
st2 = st2 + '</div></div>';

BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st2 + BodyF.innerHTML;
   $("#select_video").dialog("close");
document.getElementById("myframe").contentWindow.VideoSet(today+'_container');
myobj=$(BodyF).find("#"+today+"_container")[0];
myobj.style.zIndex = MaxZindex();
$("#myframe")[0].contentWindow.Select(today.toString());
}

function Put(){
    active = $('#active')[0].checked;
    $('#publisher_block').hide();
    $('#wait').show();

    obj = $('#myframe_conteiner')[0];
    w = obj.style.width;
    h = obj.style.height;
    tid = $("#object_id")[0].innerHTML;
    BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
    $(BodyF).find("#bgr").remove();


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
//newdocument.write('<center>');
//newdocument.write('<iframe  style="width:'+w+'; height :'+h+'" >');
st = "<div style='"+mystyle+" width :"+w+"; height :"+h+";'>";
newdocument.write(st);
newdocument.write('<title>'+title+'</title>');
newdocument.write('<div>'+body+'</div><br />');
newdocument.write('</div>');
newdocument.write('<br /><audio  preload="auto" autoplay="true" loop="loop" src=/media/'+$("#music_url")[0].innerHTML+'  /><br />');
comment = myNicEditor3.instanceById('comments_text').getContent();
newdocument.write('<div>'+comment+'</div>');
//newdocument.write('</iframe>');
//newdocument.write('</center>');
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
To_undo_conteiner();
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
st = st +'" id="'+today+'_container" style="position: absolute; z-index:4; top: 0px;  -webkit-transform:matrix(1,0,0,1,0,0);-moz-transform:matrix(1,0,0,1,0,0);-ms-transform:matrix(1,0,0,1,0,0);" />   <img  class="content" src="'+arg+'" width="50" height="50" alt="" id="'+today;
st = st +'" style=""></div>';
BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;
obj = $("#myframe")[0].contentDocument.getElementById(today.toString());
myobj=$(BodyF).find("#"+today+"_container")[0];
myobj.style.zIndex = MaxZindex();


obj.width = w;
obj.height = h;
$("#select_image").dialog("close");
To_undo_conteiner();
$("#myframe")[0].contentWindow.Select(today.toString());
}
}



function EditeMyText(){

    id = $("#text_edite_id")[0].innerHTML;
    myDiv = $("#myframe")[0].contentDocument.getElementById(id);
    myDiv.innerHTML = myNicEditor2.instanceById('text_edite_text').getContent();
    parent.$("#text_edite").dialog("close");
    To_undo_conteiner();
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
To_undo_conteiner();
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
myobj=$(BodyF).find("#"+today+"_container")[0];
myobj.style.zIndex = MaxZindex();

$("#myframe")[0].contentWindow.Select(today.toString());

}

function ColorBackground(){
To_undo_conteiner();
DeleteBackgroundImage();
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
 myobj=$(BodyF).find("#"+today+"_container")[0];
myobj.style.zIndex = MaxZindex();
  BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
  BodyF.innerHTML = st + BodyF.innerHTML;
  myobj=$(BodyF).find("#"+today+"_container")[0];
myobj.style.zIndex = MaxZindex();
$("#myframe")[0].contentWindow.Select(today.toString());

  }
}
////////////////////////////////////////////////////////////////////////////////
