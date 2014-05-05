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



function Put(){
    $("#wait").show();
    var MyDict = {'title': $("#title")[0].val(),'body': $('#myframe').contents().find("body").html(),'mtitle': $("#music_title")[0].html(),'murl': $("#music_url")[0].html(),'mauthor': $("#music_url")[0].html(),'mperformer': $("#music_performer")[0].html()};
$.ajax({
  type: "POST",
  url: "/put/",
  data: MyDict,
  success: function(msg){
alert(msg);
Screen(msg);
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {

     document.body.innerHTML = XMLHttpRequest.responseText;
  }
});


    $("#wait").hide();
}

function Screen(arg){
    html2canvas(document.body, {
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

  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {

     document.body.innerHTML = XMLHttpRequest.responseText;
  }
});

}}
)}

function Publisher(){
  document.getElementById('myframe').contentWindow.Screen();
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
alert(st);
newdocument.write(st);

newdocument.write('<title>'+title+'</title>');
newdocument.write('<div>'+body+'</div><br />');
newdocument.write('</div>');
newdocument.write('<br /><audio  preload="auto" src=/media/'+$("#music_url")[0].innerHTML+'  /><br />');
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

function AddImage(arg){

$("#undo")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].innerHTML;

if ($("#type_select_image").html() === '0'){
obj= $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
obj.style.backgroundImage = 'url(' + arg + ')';
$("#dialog").dialog("close");
}

if ($("#type_select_image").html() === '1'){

var today = NewId();

st= "<div name = 'container' onclick=";
st = st + '"Select(';
st = st +"'"+today+"');"
st = st +'" onclick="Select(';
st = st +"'"+today+"');";
st = st +'" id="'+today+'_container" style="position: absolute; z-index: 4;" />   <img  src="'+arg+'" width="50" height="50" alt="" id="'+today;
st = st +'" style=""></div>';
BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;

obj = $("#myframe")[0].contentDocument.getElementById(today.toString());
obj.width = 50*obj.naturalWidth/obj.naturalHeight;
$("#select_image").dialog("close");
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

var today = NewId();
st = '<div name = ';
st =st+"'container' onclick=";
st=st+'"Select(';
st =st + "'"+today+"');";
st=st+'" ondblclick= "EditeText(';
st = st + "'"+today+"');";


st=st+'" id = "'+today+'_container" style="position: absolute; z-index: 10; opacity: 1;" ><div><p id="'+today+'">';
st = st+text;
st = st+'</p></div></div>';

BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;


}

function ColorBackground(){

$("#undo")[0].innerHTML = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0].innerHTML;

var color = $("#selectedColor")[0].value;
obj =  $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
obj.style.backgroundColor = '#'+color;
$("#dialog").dialog("close");

}


function Select(arg){




    var mybox =$('#mybox')[0];
    if (mybox.innerHTML == (arg)){
            return;
         }

parent.document.getElementById("undo").innerHTML = document.body.innerHTML;
   $('#mybox')[0].innerHTML = arg;


    var obj = $('#'+arg);
    var offset = obj.offset();
    var objc =  $('#'+arg+'_container')[0];

try{
width = obj[0].width.toString();
height = obj[0].height.toString();
left2 = offset.left.toString();
top2 = offset.top.toString();
}catch(e) {
    width = 425;
    height = 25;
    left2 = 1;
    top2 = 15;

}


   st = '<div id="draggable_wrapper" style="width: '+ width +'px; height: '+height+'px;'+' left: '+ left2 + 'px; top: '+top2+'px;">'+'<div id="resizable-wrapper">'+objc.innerHTML+'</div></div>';

  // var st = '<div id="draggable_wrapper" style="width: '+ obj[0].width.toString() +'px; height: '+obj[0].height.toString()+'px; left: '+ offset.left.toString() + 'px; top: '+offset.top.toString()+'px;">'+'<div id="resizable-wrapper">'+objc.innerHTML+'</div></div>';

   obj.innerHTML = st;

    st =  '<div class="ui-resizeble-handle ui-resizeble-ne" unselecttable="on" style="z-index:1001;"></div><div class="ui-resizeble-handle ui-resizeble-nw" unselecttable="on" style="z-index:1002;"></div>';
    st = st + '<div class="ui-resizeble-handle ui-resizable-se ui-icon ui-icon-gripsmall-diagonal-se" unselecttable="on" style="z-index:1003;"</div><div class="ui-resizeble-handle ui-resizeble-sw" unselecttable="on" style="z-index:1004;"></div>';
    objc.innerHTML = objc.innerHTML + st;

    	var   elem = $('#'+arg);

		elem.resizable({
			aspectRatio: true,
			handles:     'ne, nw, se, sw'
		});

		elem.parent().rotatable();
		elem.parent().parent().draggable();

//elem.draggable();
    }


function Clone(){

    myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;

if (myItem === ''){
    return;
}

  obj = $('#myframe').contents().find('#'+myItem);
  AddImage(obj[0].src);


}
////////////////////////////////////////////////////////////////////////////////

