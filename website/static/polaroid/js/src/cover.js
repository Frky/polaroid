
var set_cover = function(el) {
    $.ajax("/cover/set/" + $("#gid").val() + "/" + $("img", el).attr("data-id"));
    display_alert("pinned");
}

var get_cover = function(el) {
    $.ajax("cover/" + $(el).attr("data-id")).complete(function(xhr) {
        var data = xhr.responseText.split(";");
        var gid = data[0];
        var mid = data[1];
        var ext = data[2];
        if (mid != "placeholder") {
            $("img", "." + gid).bind("error", function (evt) {
                $(this).attr("src", "/static/polaroid/img/placeholder.svg" );
            }).attr("src", "img/" + gid + "/" + mid + "-small" + ext);
        } else {
            $("img", "." + gid).attr("src", "/static/polaroid/img/placeholder.svg" );
        }
    });
}

var activate_pin = function() {
    $(".action:not(#pin)").css({"pointer-events": "none", "cursor": "default", "color": "lightgray"});
    $("#gallery").addClass("pinning");
    $("#pin").addClass("pinning");
    $("#gallery").addClass("action-in-progress");
    $(".pinning a").on('click.action', function(e) {
        e.preventDefault();
        set_cover(this);
    });
}

var deactivate_pin = function() {
    $(".action:not(#pin)").removeAttr("style");
    $(".pinning a").off('click.action');
    $("#gallery").removeClass("pinning");
    $("#pin").removeClass("pinning");
    $("#gallery").removeClass("action-in-progress");
}

$(document).ready(function() {
    $("#pin").click(function() {
        if (!$("#gallery").hasClass("pinning")) {
            activate_pin();
        } else {
            deactivate_pin();
        }
    });
});
