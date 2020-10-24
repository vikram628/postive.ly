
(function (exports, $) {
    function showEntries () {
        var data = sessionStorage.getItem("data");
        if (!data) {
            data = [
                "<h3>There are no entries. </h3>"
            ];
        }
        else {
            data = JSON.parse(data);
        }
        var $posts = $("#posts");
        $posts.empty();
        $.each(data, function (i, post) {
            $posts.append($("<div class='post'></div>").append($(post)));
        });
    }

    function addEntry (body) {
        var data = sessionStorage.getItem("data");
        if (data) data = JSON.parse(data);
        else data = [];
        body = body.replace(/\n/g, "<br/>");
        var $cont = $("<div></div>");
        $("<div class='date'></div>").text((new Date).toLocaleString()).appendTo($cont);
        $("<p></p>").html(body).appendTo($cont);
        data.unshift($cont.html());
        sessionStorage.setItem("data", JSON.stringify(data));
    }

   
    exports.addTxt = function () {
        $("#add-text").show().find("input").focus();
    };
    
    exports.okEdit = function () {
        var body = $("#add-text textarea").val();
        if (!body) {
            alert("Body is required");
            return;
        }
        addEntry(body);
        exports.cancelEdit();
        showEntries();
    };

    exports.cancelEdit = function () {
        $("#add-text input").val("");
        $("#add-text textarea").val("");
    };
    

    $(showEntries);
})(window, jQuery);
