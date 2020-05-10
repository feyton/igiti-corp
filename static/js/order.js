$(document).ready(function(){

    $(".order-detail").click(function(e) {
        var endpoint = $(this).attr("data-url");
         console.log(endpoint)
         $.ajax({
             method: 'GET',
             url: endpoint,
             success: function(data) {
                 console.log(data);
                 var target_span = $(".order_detail_id").text();
                 $(".order_detail_id").text(data.id)
             },
             error: function(error_data) {
                 console.log(error_data)
             }
         })
    })
})