var
        icon = document.getElementById("sc_icon_i"),
        num = document.getElementById("num"),
         e = document.getElementById("select");   


    //width
    function chanegiconWidth(){
        var 
        width = document.getElementById("iconwidth"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        icon.style.width = width.value + text;
    }
    function minusiconWidth(){
        var 
        width = document.getElementById("iconwidth"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        icon.style.width = width.value + text;
    }
    function plusiconWidth(){
        var 
        width = document.getElementById("iconwidth"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        icon.style.width = width.value + text;
    }
  
  //height
    function chanegiconHeight(){
        var 
        width = document.getElementById("iconheight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        icon.style.height = width.value + text;
    }
    function minusiconHeight(){
        var 
        width = document.getElementById("iconheight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        icon.style.height = width.value + text;
    }
    function plusiconHeight(){
        var 
        width = document.getElementById("iconheight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        icon.style.height = width.value + text;
    }
  
  //top
  function chanegiconTop(){
        var 
        width = document.getElementById("icontop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        icon.style.top = width.value + text;
    }
    function minusiconTop(){
        var 
        width = document.getElementById("icontop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        icon.style.top = width.value + text;
    }
    function plusiconTop(){
        var 
        width = document.getElementById("icontop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        icon.style.top = width.value + text;
    }
  
  //right
  function chanegiconRight(){
        var 
        width = document.getElementById("iconright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        icon.style.left = width.value + text;
    }
    function minusiconRight(){
        var 
        width = document.getElementById("iconright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        icon.style.left = width.value + text;
    }
    function plusiconRight(){
        var 
        width = document.getElementById("iconright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        icon.style.left = width.value + text;
    }

    
  function chanegiconBorder(){
        var 
        width = document.getElementById("iconborder"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
 
        icon.style.borderRadius = width.value + text;
    }
    function minusiconBorder(){
        var 
        width = document.getElementById("iconborder"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
 
        icon.style.borderRadius = width.value + text;
    }
    function plusiconBorder(){
        var 
        width = document.getElementById("iconborder"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
 
        icon.style.borderRadius = width.value + text;
    }