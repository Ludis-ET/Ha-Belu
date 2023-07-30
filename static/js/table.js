var
        table = document.getElementById("table"),
        num = document.getElementById("num"),
         e = document.getElementById("select");
        var mousePosition;
var offset = [0,0];
var div;
var isDown = false;

div = document.getElementById('table');
div.style.position = "absolute";

document.body.appendChild(div);

div.addEventListener('mousedown', function(e) {
    isDown = true;
    offset = [
        div.offsetLeft - e.clientX,
        div.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function() {
    isDown = false;
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();
    if (isDown) {
        mousePosition = {

            x : event.clientX,
            y : event.clientY

        };
        div.style.left = (mousePosition.x + offset[0]) + 'px';
        div.style.top  = (mousePosition.y + offset[1]) + 'px';
        document.getElementById("right").value = (mousePosition.x + offset[0]);
        document.getElementById("top").value = (mousePosition.y + offset[1]);
    }
}, true);
      


    //width
    function chanegWidth(){
        var 
        width = document.getElementById("width"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        table.style.width = width.value + text;
    }
    function minusWidth(){
        var 
        width = document.getElementById("width"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        table.style.width = width.value + text;
    }
    function plusWidth(){
        var 
        width = document.getElementById("width"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        table.style.width = width.value + text;
    }
  
  //height
    function chanegHeight(){
        var 
        width = document.getElementById("height"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        table.style.height = width.value + text;
    }
    function minusHeight(){
        var 
        width = document.getElementById("height"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        table.style.height = width.value + text;
    }
    function plusHeight(){
        var 
        width = document.getElementById("height"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        table.style.height = width.value + text;
    }
  
  //top
  function chanegTop(){
        var 
        width = document.getElementById("top"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        table.style.top = width.value + text;
    }
    function minusTop(){
        var 
        width = document.getElementById("top"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        table.style.top = width.value + text;
    }
    function plusTop(){
        var 
        width = document.getElementById("top"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        table.style.top = width.value + text;
    }
  
  //right
  function chanegRight(){
        var 
        width = document.getElementById("right"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        table.style.left = width.value + text;
    }
    function minusRight(){
        var 
        width = document.getElementById("right"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        table.style.left = width.value + text;
    }
    function plusRight(){
        var 
        width = document.getElementById("right"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        table.style.left = width.value + text;
    }
  
    
  //size
  function chanegFontSize(){
        var 
        width = document.getElementById("size"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='one']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function minusFontSize(){
        var 
        width = document.getElementById("size"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        var elms = document.querySelectorAll("[id='one']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function plusFontSize(){
        var 
        width = document.getElementById("size"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        var elms = document.querySelectorAll("[id='one']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
  

    //family
  function chanegFontFamily(){
        var 
        width = document.getElementById("family"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='one']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontFamily = width.value;
    }
        


//size
  function chanegnFontSize(){
        var 
        width = document.getElementById("nsize"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='two']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function minusnFontSize(){
        var 
        width = document.getElementById("nsize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        var elms = document.querySelectorAll("[id='two']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function plusnFontSize(){
        var 
        width = document.getElementById("nsize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        var elms = document.querySelectorAll("[id='two']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
  

    //number family
  function chanegnFontFamily(){
        var 
        width = document.getElementById("nfamily"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='two']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontFamily = width.value;
    }
    




    
  function chanegBorder(){
        var 
        width = document.getElementById("border"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='one']");
        var elmss = document.querySelectorAll("[id='two']");
 
        table.style.border = width.value + text + " solid black";
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.border = width.value + text + " solid black";
        for(var i = 0; i < elmss.length; i++) 
            elmss[i].style.border = width.value + text + " solid black";
    }
    function minusBorder(){
        var 
        width = document.getElementById("border"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        var elms = document.querySelectorAll("[id='one']");
        var elmss = document.querySelectorAll("[id='two']");
 
        table.style.border = width.value + text + " solid black";
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.border = width.value + text + " solid black";
        for(var i = 0; i < elmss.length; i++) 
            elmss[i].style.border = width.value + text + " solid black";
    }
    function plusBorder(){
        var 
        width = document.getElementById("border"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        var elms = document.querySelectorAll("[id='one']");
        var elmss = document.querySelectorAll("[id='two']");
 
        table.style.border = width.value + text + " solid black";
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.border = width.value + text + " solid black";
        for(var i = 0; i < elmss.length; i++) 
            elmss[i].style.border = width.value + text + " solid black";
    }