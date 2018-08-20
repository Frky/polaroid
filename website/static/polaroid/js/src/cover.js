
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
    $(".pinning a").click(function(e) {
        if (!$("#gallery").hasClass("action-in-progress")) {
            return;
        }
        e.preventDefault();
        set_cover(this);
    });
}

$(document).ready(function() {
    $("#pin").click(function() {
        $("#pin").toggleClass("pinning");
        $("#gallery").toggleClass("pinning");
        $("#gallery").toggleClass("action-in-progress");
        activate_pin();
    });
});
