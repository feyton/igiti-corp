$(document).ready(function () {
    $('.post-wrapper').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        nextArrow: document.getElementById('next'),
        prevArrow: document.getElementById('prev'),
        arrows: true,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
    $("#blog_search_form").submit(function (e) {
        var query = $("#blog_search").val();
        if (query != '') {
            console.log(query)

        } else {
            e.preventDefault();
        }
    });
    $(".order-detail").click(function(e) {
        var endpoint = $(this).attr("data-url");
         console.log(endpoint)
         $.ajax({
             method: 'GET',
             url: endpoint,
             success: function(data) {
                 console.log(data);
                //  var target_span = $(".order_detail_id").text();
                 $(".order_detail_id").text(data.id);
                 var total_span = $(".order_total_amount").text();
                 $(".order_total_amount").text(data.total);
                 console.log(total_span);
                 $('#cancel_order').attr("href", data.cancel);
                 $(".total_items_count").text(data.items)
             },
             error: function(error_data) {
                 console.log(error_data)
             }
         })
    });
    $("#remove_quantity").click(function () {
        var current = $("#quantity_5ea093f3a2b82").val();
        if (current > 1) {
            var change_value = current -= 1;
            $("#quantity_5ea093f3a2b82").val('');
            $("#quantity_5ea093f3a2b82").val(change_value)
        } else {
            $("#quantity_5ea093f3a2b82").val(1)
        }
    });
    $('#add_quantity').click(function () {
        var current = Number($("#quantity_5ea093f3a2b82").val());
        if (current >= 1 && current < 9) {
            var added_value = current += 1;
            $("#quantity_5ea093f3a2b82").val('');
            $("#quantity_5ea093f3a2b82").val(added_value);
        } else {
            $("#quantity_5ea093f3a2b82").val(9);
            console.log('Maximum allowed quantity is 9 Kg')
        }

    });
})
