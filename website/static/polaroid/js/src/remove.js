
var remove = function(el) {
    if ($(el).parent().parent().parent().hasClass("liked-galleries")) {
        unlike($(el).attr("title"));
        $(el).remove();
    } else if ($(el).hasClass("img")) {
        $.ajax({url: "/rm/img/" + $("img", el).attr("data-id")}).complete(function(xhr) {
            if (xhr.responseText == "OK") {
                $(el).remove();
                arrange_all();
                display_alert("removed");
            }
        });
    } else {
        $.ajax({url: "/rm/gl/" + $(el).attr("title")}).complete(function(xhr) {
            if (xhr.responseText == "OK") {
                $(el).parent().remove();
            }
        });
    }
}

var activate_rm = function() {
    console.log("AYO");
    $(".removing a").click(function(e) {
        console.log("YOLO ?");
        if (!$("#gallery").hasClass("action-in-progress")) {
            return;
        }
        console.log("YOLO");
        e.preventDefault();
        remove(this);
    });
}

$(document).ready(function() {
    $("#remove").click(function() {
        $("#remove").toggleClass("removing");
        $("#gallery").toggleClass("removing");
        $("#gallery").toggleClass("action-in-progress");
        activate_rm();
    });
});
