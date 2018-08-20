
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
    $(".action:not(#remove)").css({"pointer-events": "none", "cursor": "default", "color": "lightgray"});
    $("#gallery").addClass("removing");
    $("#remove").addClass("removing");
    $("#gallery").addClass("action-in-progress");
    $(".removing a").on('click.action', function(e) {
        e.preventDefault();
        remove(this);
    });
}

var deactivate_rm = function() {
    $(".action:not(#remove)").removeAttr("style");
    $(".removing a").off('click.action');
    $("#gallery").removeClass("removing");
    $("#remove").removeClass("removing");
    $("#gallery").removeClass("action-in-progress");
}

$(document).ready(function() {
    $("#remove").click(function() {
        if (!$("#gallery").hasClass("removing")) {
            activate_rm();
        } else {
            deactivate_rm();
        }
    });
});
