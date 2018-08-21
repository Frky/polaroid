
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
    $(".cropping a").click(function(e) {
        if (!$("#gallery").hasClass("action-in-progress")) {
            return;
        }
        e.preventDefault();
        crop(this);
    });
}

$(document).ready(function() {
    $("#crop").click(function() {
        $("#crop").toggleClass("cropping");
        $("#gallery").toggleClass("cropping");
        $("#gallery").toggleClass("action-in-progress");
        activate_crop();
    });
});
