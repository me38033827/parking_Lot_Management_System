function password_confirm() { // for confirm the password
    var passowrd = document.getElementById("myPass").value;

    $.ajax({
        url: '/park/delete',
        type: 'DELETE',
        headers: { 'password': passowrd },
        complete: function(xhr, textStatus) {
            if(xhr.status == 400)
                alert("Password Error.");
            else 
                window.location.href = "/park/login";
        } 
    });
}

var cars = "";

function draw_cars() { // draw the cars
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var img;
    img = new Image();
    img.src = "/static/assets/static/images/car.png";

    if (cars == "") {
        $.ajax({
            url: '/park/positions',
            type: 'GET',
            success: function(data, textStatus) {
                cars = JSON.parse(data);
                $("#carNum").html(Number(cars.length).toFixed(0) + " Cars");
                $("#percent").html(Number(cars.length / 28 * 100).toFixed(2) + "%");
                $("#percentProgress").attr("aria-valuenow", Number(cars.length / 28 * 100).toFixed(2));
                $("#percentProgress").attr("style", "width:" + Number(cars.length / 28 * 100).toFixed(2) + "%");
                draw_(cars);
            }
        });
    }
    else {
        draw_(cars);
    }


    function draw_(cars) {
        for (var i = 0; i < cars.length; i++) {
            var x = cars[i]['xCoord'] * c.width / 1315; 
            var y = cars[i]['yCoord'] * c.width / 1315;
            var rot = cars[i]['rot'] / 180 * 3.1416;
            drawImage(img, x, y, c.width / 1315, rot);
        }
    }

    function drawImage(image, x, y, scale, rotation){
        ctx.setTransform(scale, 0, 0, scale, x, y); // sets scale and origin
        ctx.rotate(rotation);
        ctx.drawImage(image, -image.width / 2, -image.height / 2);
    } 
}

function send_notification() { // send notification to your device
    $.ajax({
        url: '/park/record',
        type: 'GET',
        complete: function(xhr, textStatus) {
            if (xhr.status == 200)
                alert("Send successfully. Please check your email");
            else
                alert("Error!");
        }
    });
}

function init_user() { // init the web page. add park lot information
    $.ajax({
        url: '/park/parktime',
        type: 'GET',
        success: function(data, textStatus, request) {
            $("#avgParking").html(Number(request.getResponseHeader("meantime")).toFixed(2) + "min");
            $("#avgParkingbar").attr("aria-valuenow", Number(request.getResponseHeader("meantime") / 24 / 60 * 100).toFixed(2));
            $("#avgParkingbar").attr("style", "width:" + Number(request.getResponseHeader("meantime") / 24 / 60 * 100).toFixed(2) + "%");
        }
    });
}

var week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

function init() { // get weather and gas price
    $.ajax({
        url: '/park/weather',
        type: 'GET',
        success: function(data, textStatus, request) {
            $("#temp").html(data["main"]["temp"] + "<sup>°F</sup>");
            $("#weather").html(data["weather"][0]["main"]);
            var d = new Date();
            var n = d.getDay();
            $("#Today").html(week[n]);
            $("#date").html(d.toDateString());
            $("#wind").html(data["wind"]["speed"] + "km/h");
            d = new Date(data["sys"]["sunrise"] * 1000);
            $("#sunrise").html(d.toTimeString());
            $("#pressure").html(data["main"]["pressure"] + "hPa");
            $("#weatherIcon").attr("src", "https://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png")
        }
    });

    $.ajax({
        url: '/park/gas',
        type: 'GET',
        success: function(data, textStatus, request) {
            $("#reg").html("Regular: " + $('regPrice', data).text());
            $("#mid").html("Mid-grade: " + $('midPrice', data).text());
            $("#pre").html("Premium: " + $('prePrice', data).text());
        }
    });
}

function navigate_car() { // get route of car
    $.ajax({
        url: '/park/navigation',
        type: 'GET',
        success: function(data, textStatus, request) {
            route = JSON.parse(data);
            draw_route(route, 'rgb(103, 37, 178)');
        }
    });
}

function navigate_user() { // get route of user
    $.ajax({
        url: '/park/navigation?user',
        type: 'GET',
        success: function(data, textStatus, request) {
            route = JSON.parse(data);
            draw_route(route, 'rgb(234, 147, 32)');
        }
    });
}

function draw_route(route, color) { // draw the route to the canvas
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.strokeStyle = color;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 5;
    ctx.resetTransform(); // sets scale and origin
    ctx.rotate(0);
    ctx.beginPath();
    var ratio = c.width / 1315.0;
    ctx.moveTo(route[0][0] * ratio, route[0][1] * ratio);
    for (var i = 1; i < route.length; i++) {
        ctx.lineTo(route[i][0] * ratio, route[i][1] * ratio);
    }
    ctx.stroke();
}

function resizeCanvas() { // when window resize, change the canvas's size
    $("#myCanvas").attr("width", $("#test").width());
    $("#myCanvas").attr("height", $("#myCanvas").width() * 9 / 13);
    var c = document.getElementById("myCanvas");
    var cxt = c.getContext("2d");
    cxt.drawImage(img, 0, 0, c.width, c.height);
    draw_cars();
    draw_car_route = false;
};
