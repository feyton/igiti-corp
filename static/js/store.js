$(document).ready(function () {
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