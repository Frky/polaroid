
var img_cropped;

var crop = function(el) {
    $.ajax({url: "/crop/img/" + $("img", el).attr("data-id")}).complete(function(xhr) {
            data = xhr.responseText.split(";");
            if (data[0] == "OK") {
                img = $('*[data-id="' + data[1] + '"]')[0];
                img.src = img.src + "?" + new Date().getTime();
                img.removeAttribute("width");
                img.removeAttribute("height");
                setTimeout(arrange_all, 1000);
                display_alert("cropped");
            }
    });
}

var activate_crop = function() {
    $(".action:not(#crop)").css({"pointer-events": "none", "cursor": "default", "color": "lightgray"});
    $("#gallery").addClass("cropping");
    $("#crop").addClass("cropping");
    $("#gallery").addClass("action-in-progress");
    $(".cropping a").on('click.action', function(e) {
        e.preventDefault();
        crop(this);
    });
}

var deactivate_crop = function() {
    $(".action:not(#crop)").removeAttr("style");
    $(".cropping a").off('click.action');
    $("#gallery").removeClass("cropping");
    $("#crop").removeClass("cropping");
    $("#gallery").removeClass("action-in-progress");
}

$(document).ready(function() {
    $("#crop").click(function() {
        if (!$("#gallery").hasClass("cropping")) {
            activate_crop();
        } else {
            deactivate_crop();
        }
    });
});
