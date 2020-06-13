$(document).ready(function () {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});

function getData() {
    var response;
    $.ajax({
        async: false,
        type: "GET",
        url: "http://127.0.0.1:8000/get_data",
        dataType: "json",
        success: function (data) {
            response = data;
        },
        error: function (e) {
            console.log(e);
        }
    });

    return response;
}