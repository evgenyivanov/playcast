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



function Screen(){
    html2canvas(document.body, {
  onrendered: function(canvas) {
    document.body.appendChild(canvas);
    dataURL = canvas.toDataURL("image/png");

        alert(dataURL);
        obj=$(canvas);
obj.remove();
  },

});


//[0].getImageData();
//alert(ImageData);
}

function Publisher(){
  document.getElementById('myframe').contentWindow.Screen();
}


function Preview(){
title = $("#title")[0].value;
body =  $('#myframe').contents().find("body").html();
newwindow=window.open("",title);
newdocument=newwindow.document;
newdocument.write('<head><script src="/static/js/audio.min.js"></script><script> audiojs.events.ready(function() {var as = audiojs.createAll(); });</script></head>');
newdocument.write('<BODY>');

newdocument.write('<title>'+title+'</title>');
newdocument.write('<div>'+body+'</div><br />');
hh = document.body.scrollHeight;
hh = hh + 1;
newdocument.write('<div style="position: absolute; top : '+hh.toString()+'px;"><audio  preload="auto" src=/media/'+$("#music_url")[0].innerHTML+'  /><br /></div>');
hh = hh + 50;
comment = myNicEditor3.instanceById('comments_text').getContent();

newdocument.write('<div style="position: absolute; top : '+hh.toString()+'px;">'+comment+'</div>');
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

if ($("#type_select_image").html() === '0'){
obj= $('#myframe').contents().find('#background');
obj.css('background-image', 'url(' + arg + ')');
$("#dialog").dialog("close");
}

if ($("#type_select_image").html() === '1'){

var today = NewId();

st= "<div name = 'container' onclick=";
st = st + '"Select(';
st = st +"'"+today+"');"
st = st +'" onclick="Select(';
st = st +"'"+today+"');";
st = st +'" id="'+today+'_container" style="position: absolute; z-index: 4;" />   <img src="'+arg+'" width="50" height="50" alt="" id="'+today;
st = st +'" style=""></div>';
BodyF = $("#myframe")[0].contentDocument.getElementsByTagName('body')[0];
BodyF.innerHTML = st + BodyF.innerHTML;

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
myItem = obj = $('#myframe').contents().find('#mybox')[0].innerHTML;

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
var color = $("#selectedColor")[0].value;
obj = $('#myframe').contents().find('#background');
obj[0].style.backgroundColor = '#'+color;
$("#dialog").dialog("close");

}

function BackgroundReSize(){

    var   elem = $('#background');
    elem.resizable({
			aspectRatio: true,
			handles:     'ne, nw, se, sw'
		});
		elem.parent().draggable();
}

function Select(arg){

    var mybox =$('#mybox')[0];
    if (mybox.innerHTML == (arg)){
            return;
         }

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

////////////////////////////////////////////////////////////////////////////////

