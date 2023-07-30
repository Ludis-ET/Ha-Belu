var
        stname = document.getElementById("st_name_p"),
        num = document.getElementById("num"),
         e = document.getElementById("select");

  //top
  function chanegnameTop(){
        var 
        width = document.getElementById("nametop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        stname.style.top = width.value + text;
    }
    function minusnameTop(){
        var 
        width = document.getElementById("nametop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        stname.style.top = width.value + text;
    }
    function plusnameTop(){
        var 
        width = document.getElementById("nametop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        stname.style.top = width.value + text;
    }



    
  //right
  function chanegnameRight(){
        var 
        width = document.getElementById("nameright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        stname.style.left = width.value + text;
    }
    function minusnameRight(){
        var 
        width = document.getElementById("nameright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        stname.style.left = width.value + text;
    }
    function plusnameRight(){
        var 
        width = document.getElementById("nameright"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        stname.style.left = width.value + text;
    }
  
  


    
  //size
  function chanegnameFontSize(){
        var 
        width = document.getElementById("namesize"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='st_name_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function minusnameFontSize(){
        var 
        width = document.getElementById("namesize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        var elms = document.querySelectorAll("[id='st_name_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function plusnameFontSize(){
        var 
        width = document.getElementById("namesize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        var elms = document.querySelectorAll("[id='st_name_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
  

    //family
  function chanegnameFontFamily(){
        var 
        width = document.getElementById("namefamily"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='st_name_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontFamily = width.value;
    }
        