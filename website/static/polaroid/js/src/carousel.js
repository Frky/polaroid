
var enter_carousel = function(el) {
    $("li", "#gallery-carousel").removeClass("active");
    $(".carousel-item", "#gallery-carousel").removeClass("active");
    $("li[data-img=" + $(el).attr("data-id") + "]", "#gallery-carousel").addClass("active");
    $(".carousel-item[data-img=" + $(el).attr("data-id") + "]", "#gallery-carousel").addClass("active");
    $("#gallery-carousel").removeClass("hidden");
    $("#gallery").addClass("hidden");
    $("header").addClass("hidden");
    $("body").addClass("carousel");
    noty_carousel = new Noty({
        type: "info",
        layout: "top",
        text: "<center>To close the carousel, click the photo or press Esc.</center>",
        closeWith: ["click", "button"]
    }).show();
};

var exit_carousel = function() {
    $("#gallery-carousel").addClass("hidden");
    $("#gallery").removeClass("hidden");
    $("header").removeClass("hidden");
    $("body").removeClass("carousel");
    if (!noty_carousel.closed)
        noty_carousel.close()
}

$(document).ready(function() {
    $("img", "#gallery-carousel").each(function() {
        $(this).attr("src", $(this).attr("data-src"));
    });
    $("img").click(function(e) {
        e.preventDefault();
        if ($("#gallery").hasClass("action-in-progress"))
            return;
        if ($("#gallery").hasClass("hidden")) {
            exit_carousel();
        } else {
            enter_carousel(this);
        }
    });
    $(document).keyup(function(e){
        if(e.keyCode === 27 && $("#gallery").hasClass("hidden"))
            exit_carousel()
    });
});
