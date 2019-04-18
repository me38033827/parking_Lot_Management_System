function initData() { // init web page for admin, including some statistic data
    var today = new Date("2019-03-18");
    var nums = new Array(0);
    today.toISOString().slice(0, 10);
    for (var i = 0; i < 8; i++) { // every 30 days, how many cars enter the parking lot
        var nowTime = today.getTime();
        var ms = 24 * 3600 * 1000 * -30;
        var lastMonth = new Date(nowTime + ms);
        $.ajax({
            url: '/park/number?start=' + lastMonth.toISOString().slice(0, 10) + '&end=' +  today.toISOString().slice(0, 10),
            type: 'GET',
            async: false,
            success: function(data, textStatus, request) {
                nums.push(request.getResponseHeader("number"));
            }
        });
        today = lastMonth;
    }
    nums.reverse();
    $("#last30day").sparkline(nums, {type:"bar",height:"20",barWidth:"3",resize:!0,barSpacing:"3",barColor:"#4caf50"});
    $("#percent30").html(Number((nums[7] - nums[6]) / nums[6] * 100).toFixed(2) + "%");

    today = new Date("2019-03-18");
    var nowTime = today.getTime();
    var ms = 24 * 3600 * 1000 * 1;
    today = new Date(nowTime + ms);
    nums = new Array(0);
    for (var i = 0; i < 7; i++) { // every 7 days, how many cars enter the parking lot
        nowTime = today.getTime();
        ms = 24 * 3600 * 1000 * -1;
        lastDay = new Date(nowTime + ms);
        $.ajax({
            url: '/park/number?start=' + lastDay.toISOString().slice(0, 10) + '&end=' +  today.toISOString().slice(0, 10),
            type: 'GET',
            async: false,
            success: function(data, textStatus, request) {
                nums.push(request.getResponseHeader("number"));
            }
        });
        today = lastDay;
    }
    nums.reverse();
    $("#thisWeek").sparkline(nums, { type: "bar", height: "20", barWidth: "3", resize: !0, barSpacing: "3", barColor: "#9675ce" });
    $("#percentDay").html(Number((nums[6] - nums[5]) / nums[5] * 100).toFixed(2) + "%");

    today = new Date("2019-03-18");
    nums = new Array(0);
    for (var i = 0; i < 8; i++) { // every 30 days, how much did the park lot get.
        var nowTime = today.getTime();
        var ms = 24 * 3600 * 1000 * -30;
        var lastMonth = new Date(nowTime + ms);
        $.ajax({
            url: '/park/income?start=' + lastMonth.toISOString().slice(0, 10) + '&end=' +  today.toISOString().slice(0, 10),
            type: 'GET',
            async: false,
            success: function(data, textStatus, request) {
                nums.push(request.getResponseHeader("income"));
            }
        });
        today = lastMonth;
    }
    nums.reverse();
    $("#last30day_income").sparkline(nums, { type: "bar", height: "20", barWidth: "3", resize: !0, barSpacing: "3", barColor: "#9675ce" });
    $("#percent30_income").html(Number((nums[7] - nums[6]) / nums[6] * 100).toFixed(2) + "%");

    today = new Date("2019-03-18");
    nowTime = today.getTime();
    ms = 24 * 3600 * 1000 * 1;
    today = new Date(nowTime + ms);
    nums = new Array(0);
    for (var i = 0; i < 7; i++) { // every 7 days, how much did the park lot get.
        nowTime = today.getTime();
        ms = 24 * 3600 * 1000 * -1;
        lastDay = new Date(nowTime + ms);
        $.ajax({
            url: '/park/income?start=' + lastDay.toISOString().slice(0, 10) + '&end=' +  today.toISOString().slice(0, 10),
            type: 'GET',
            async: false,
            success: function(data, textStatus, request) {
                nums.push(request.getResponseHeader("income"));
            }
        });
        today = lastDay;
    }
    nums.reverse();
    $("#thisWeek_income").sparkline(nums, { type: "bar", height: "20", barWidth: "3", resize: !0, barSpacing: "3", barColor: "#9675ce" });
    $("#percentDay_income").html(Number((nums[6] - nums[5]) / nums[5] * 100).toFixed(2) + "%");

    today = new Date("2019-03-18");
    nums = new Array(0);
    var nowTime = today.getTime(); // get usage information
    var ms = 24 * 3600 * 1000 * -30;
    var lastMonth = new Date(nowTime + ms);
    $.ajax({
        url: '/park/usage?start=' + lastMonth.toISOString().slice(0, 10) + '&end=' +  today.toISOString().slice(0, 10),
        type: 'GET',
        success: function(data, textStatus, request) {
            $("#usage").html(Number(request.getResponseHeader("usage") * 100).toFixed(2) + "%");
            $("#percentProgressUsage").attr("aria-valuenow", Number(request.getResponseHeader("usage") * 100).toFixed(2));
            $("#percentProgressUsage").attr("style", "width:" + Number(request.getResponseHeader("usage") * 100).toFixed(2) + "%");
        }
    });
    today = lastMonth;
}
