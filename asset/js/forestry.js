$(document).ready(function () {
    $("#blog_search_form").submit(function (e) {
        var query = $("#blog_search").val();
        if (query != '') {
            console.log(query)

        } else {
            e.preventDefault();
        }
    })
})