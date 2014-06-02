
function Matrix2(){

    myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;
    ob=$("#myframe")[0].contentDocument.getElementById(myItem+'_container');
    st = 'matrix('+ $('#m1')[0].value.toString()+','+ $('#m2')[0].value.toString()+','+ $('#m3')[0].value.toString()+',';
    st = st + + $('#m4')[0].value.toString()+','+ $('#m5')[0].value.toString()+','+ $('#m6')[0].value.toString()+')';
    ob.style.{{Transform}} = st;
}

function Matrix1(){
    myItem =  $('#myframe').contents().find('#mybox')[0].innerHTML;
    ob=$("#myframe")[0].contentDocument.getElementById(myItem+'_container');

    st = ob.style.{{Transform}};
    st = st.replace('matrix(','').replace(')','');
    var res = st.split(",");
     $('#m1')[0].value = parseFloat(res[0]);
     $('#m2')[0].value = parseFloat(res[1]);
     $('#m3')[0].value = parseFloat(res[2]);
     $('#m4')[0].value = parseFloat(res[3]);
     $('#m5')[0].value = parseFloat(res[4]);
     $('#m6')[0].value = parseFloat(res[5]);


    $("#matrix").dialog("open");
}



function SumMatrix(a,b){
a = a.replace('matrix(','').replace(')','');
if (a.toString()==="" ){
a = '1,1,1,1,1,1';}

var resA = a.split(",");
b = b.replace('matrix(','').replace(')','');
if (b.toString()===""){
b = '1,1,1,1,1,1';}
var resB = b.split(",");

if (parseFloat(resA[0])==1 && parseFloat(resA[1])==0 && parseFloat(resA[2])==0 && parseFloat(resA[3])== 1 && parseFloat(resA[4]) == 0 && parseFloat(resA[5]) == 0){

   st = 'matrix('+resB[0]+','+resB[1].toString()+','+resB[2].toString()+','+resB[3]+','+resB[4]+','+resB[5]+ ')';

   return st;}




if (parseFloat(resB[0])==1 && parseFloat(resB[1])==0 && parseFloat(resB[2])==0 && parseFloat(resB[3])== 1 && parseFloat(resB[4]) == 0 && parseFloat(resB[5]) == 0){
    st = 'matrix('+resA[0]+','+resA[1]+','+resA[2]+','+resA[3]+','+resA[4]+','+resA[5]+ ')';

    return st;}


c0 = parseFloat(resA[0])*parseFloat(resB[0]);
c1 = parseFloat(resA[1])*parseFloat(resB[1]);
c2 = parseFloat(resA[2])*parseFloat(resB[2]);
c3 = parseFloat(resA[3])*parseFloat(resB[3]);
c4 = parseFloat(resA[4])*parseFloat(resB[4]);
c5 = parseFloat(resA[5])*parseFloat(resB[5]);

st = 'matrix('+c0.toString()+','+c1.toString()+','+c2.toString()+','+c3.toString()+','+c4.toString()+','+c5.toString()+ ')';

return st;
}


function Select(arg){

    var mybox =$('#mybox')[0];
    if (mybox.innerHTML == (arg)){
            return;
         }
 $("#matrix").dialog("close");


  $(".ui-resizable-handle").remove();
  $(".ui-rotatable-handle").remove();

  $(".container").each(function a(){

     cont = $(this).find(".content").parent()[0].innerHTML;



      try{
      obj = $(this).find(".ui-wrapper")[0];



      if (obj.style.left == "auto"){obj.style.left ="0px";}
      if (obj.style.top == "auto"){obj.style.top ="0px";}
      this.style.left = (parseInt(this.style.left) + parseInt(obj.style.left)).toString()+"px";

      this.style.top =  (parseInt(this.style.top) + parseInt(obj.style.top)).toString()+"px";
      this.style.width = (parseInt(this.style.width) + parseInt(obj.style.width)).toString();
      this.style.height = (parseInt(this.style.height) + parseInt(obj.style.height)).toString();

      transform = SumMatrix(this.style.{{Transform}},obj.style.{{Transform}}).toString();


      this.style.webkitTransform = transform;
      this.style.MozTransform = transform;
      this.style.msTransform = transform;


      this.innerHTML = cont;} catch(e){};
  }
      );




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


   obj.innerHTML = st;

    st =  '<div class="ui-resizeble-handle ui-resizeble-ne" unselecttable="on" style="z-index:1001;"></div><div class="ui-resizeble-handle ui-resizeble-nw" unselecttable="on" style="z-index:1002;"></div>';
    st = st + '<div class="ui-resizeble-handle ui-resizable-se ui-icon ui-icon-gripsmall-diagonal-se" unselecttable="on" style="z-index:1003;"</div><div class="ui-resizeble-handle ui-resizeble-sw" unselecttable="on" style="z-index:1004;"></div>';
    objc.innerHTML = objc.innerHTML + st;


    	var   elem = $('#'+arg);

		elem.resizable({
		//	aspectRatio: true,
			handles:     'ne, nw, se, sw'
		});

		elem.parent().rotatable();

		elem.parent().parent().draggable();



    }



////////////////////////////////////////////////////////////////////////////////

