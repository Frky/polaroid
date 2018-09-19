var download = function(el) {
    var dl = $("<a download>").attr("href", $(el).attr("href"))
        .attr("download", $(el).attr("href").substr(5).replace(".jpg", "") + ".jpg")
        .insertBefore(el);
    dl[0].click();
    dl.remove();
}

var activate_download = function() {
    $(".action:not(#download)").css({"pointer-events": "none", "cursor": "default", "color": "lightgray"});
    $("#gallery").addClass("downloading");
    $("#download").addClass("downloading");
    $("#gallery").addClass("action-in-progress");
    $(".downloading a").on('click.action', function(e) {
        e.preventDefault();
        download(this);
    });
}

var deactivate_download = function() {
    $(".action:not(#download)").removeAttr("style");
    $(".downloading a").off('click.action');
    $("#gallery").removeClass("downloading");
    $("#download").removeClass("downloading");
    $("#gallery").removeClass("action-in-progress");
}

$(document).ready(function() {
    $("#download").click(function() {
        if (!$("#gallery").hasClass("downloading")) {
            activate_download();
        } else {
            deactivate_download();
        }
    });
});
