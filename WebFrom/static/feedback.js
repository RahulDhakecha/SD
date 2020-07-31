$(document).ready(function () {

    $(".zer").click(function () {
        $(".zero").show();
        $(".extra").hide();
    });

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
    });
});
