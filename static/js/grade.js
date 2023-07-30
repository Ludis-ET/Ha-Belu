var
        grade = document.getElementById("st_grade_p"),
        num = document.getElementById("num"),
         e = document.getElementById("select");

  //top
  function chaneggradeTop(){
        var 
        width = document.getElementById("gradetop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        grade.style.top = width.value + text;
    }
    function minusgradeTop(){
        var 
        width = document.getElementById("gradetop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        grade.style.top = width.value + text;
    }
    function plusgradeTop(){
        var 
        width = document.getElementById("gradetop"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        grade.style.top = width.value + text;
    }



    
  //right
  function chaneggradeRight(){
        var 
        width = document.getElementById("graderight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        grade.style.left = width.value + text;
    }
    function minusgradeRight(){
        var 
        width = document.getElementById("graderight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        grade.style.left = width.value + text;
    }
    function plusgradeRight(){
        var 
        width = document.getElementById("graderight"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        grade.style.left = width.value + text;
    }
  
  


    
  //size
  function chaneggradeFontSize(){
        var 
        width = document.getElementById("gradesize"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='st_grade_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function minusgradeFontSize(){
        var 
        width = document.getElementById("gradesize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (width.value - num.value);
        var elms = document.querySelectorAll("[id='st_grade_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
    function plusgradeFontSize(){
        var 
        width = document.getElementById("gradesize"),
     value = e.value;
    var text = e.options[e.selectedIndex].text;
        width.value = (+(width.value) + +(num.value));
        var elms = document.querySelectorAll("[id='st_grade_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontSize = width.value + text;
    }
  

    //family
  function chaneggradeFontFamily(){
        var 
        width = document.getElementById("gradefamily"),
        value = e.value;
        var text = e.options[e.selectedIndex].text;
        var elms = document.querySelectorAll("[id='st_grade_p']");
 
        for(var i = 0; i < elms.length; i++) 
            elms[i].style.fontFamily = width.value;
    }