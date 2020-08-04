$(document).ready(function () {

    var data_list = []
    var allVals = [];
    $(".zer").click(function () {
        $(".zero").show();
        $(".extra").hide();
    });

    var first_anchors = document.querySelectorAll('.first');
    var second_anchors = document.querySelectorAll('.second');
    var third_anchors = document.querySelectorAll('.third');
    var fourth_anchors = document.querySelectorAll('.fourth');
    // var fifth_anchors = document.querySelectorAll('.container');
    var sixth_anchors = document.querySelectorAll('.sixth');
    // var seventh_anchors = document.querySelectorAll('.textbox');

    for (var i=0; i<first_anchors.length; i++) {
        first_anchors[i].addEventListener('click', handler, false);
    }
    for (var i=0; i<second_anchors.length; i++) {
        second_anchors[i].addEventListener('click', handler, false);
    }
    for (var i=0; i<third_anchors.length; i++) {
        third_anchors[i].addEventListener('click', handler, false);
    }
    for (var i=0; i<fourth_anchors.length; i++) {
        fourth_anchors[i].addEventListener('click', handler, false);
    }
//    for (var i=0; i<fifth_anchors.length; i++) {
//        fifth_anchors[i].addEventListener('click', handler, false);
//    }
    for (var i=0; i<sixth_anchors.length; i++) {
        sixth_anchors[i].addEventListener('click', handler, false);
    }
    // for (var i=0; i<seventh_anchors.length; i++) {
    //     seventh_anchors[i].addEventListener('click', handler, false);
    // }

    function handler() {
        data_list.push(this.text)
    }

//     function checkBoxClickHandler() {
//         console.log("Coming Here")
// //        data_list.push(this.text)
//     }

    $(".first").click(function () {
        $(".one").show();

        var elem = document.getElementById("myBar");
        var width = 0;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 15) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }

    });

    $(".second").click(function () {
        $(".two").show();
        var elem = document.getElementById("myBar");
        var width = 15;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 30) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".third").click(function () {
        $(".three").show();
        var elem = document.getElementById("myBar");
        var width = 30;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 45) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".fourth").click(function () {
        $(".four").show();
        var elem = document.getElementById("myBar");
        var width = 45;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 60) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".fifth").click(function () {
          allVals = [];
     $('#formsimser :checked').each(function() {
       allVals.push($(this).val());
     });
     alert("Values " + allVals);
        $(".five").show();
        var elem = document.getElementById("myBar");
        var width = 60;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 75) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".sixth").click(function () {
        $(".six").show();
        var elem = document.getElementById("myBar");
        var width = 75;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 90) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });

    $(".seventh").click(function () {
        var sugg = document.getElementById("suggestion").value;
        alert(sugg);
        $(".seven").show();
                $(".six").hide();

        var elem = document.getElementById("myBar");
        var width = 90;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 100) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
        $.ajax({
          type: "POST",
          async: "true",
          contentType: "application/json;charset=utf-8",
          url: "/feedback/RJ-ODR-2020-2037",
          traditional: "true",
          data: JSON.stringify(data_list),
          dataType: "json"
          });
    });
});
