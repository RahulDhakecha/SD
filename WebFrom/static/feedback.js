$(document).ready(function () {

    $(".zer").click(function () {
        $(".zero").toggle(500);
    });

    $(".first").click(function () {

        $(".one").toggle(500);

        var elem = document.getElementById("myBar");
        var width = 0;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 17) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }

    });

    $(".second").click(function () {
        $(".two").toggle(500);
        var elem = document.getElementById("myBar");
        var width = 17;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 34) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".third").click(function () {
        $(".three").toggle(500);
        var elem = document.getElementById("myBar");
        var width = 34;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 51) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".fourth").click(function () {
        $(".four").toggle(500);
        var elem = document.getElementById("myBar");
        var width = 51;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 68) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".fifth").click(function () {
        $(".five").toggle(500);
        var elem = document.getElementById("myBar");
        var width = 68;
        var id = setInterval(frame, 10);

        function frame() {
            if (width >= 85) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    });
    $(".sixth").click(function () {
        $(".six").toggle(500);
        var elem = document.getElementById("myBar");
        var width = 85;
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
