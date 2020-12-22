demo = {
  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },
  
};
$(document).ready(function(e) {
  $("#id_image1").change(function () {
    var filePath = $(this)[0].files[0].name;
    $("#image1_label").text(filePath);
    $('#image1_clear_div').hide();
});
$("#id_image2").change(function () {
    var filePath = $(this)[0].files[0].name;
    $("#image2_label").text(filePath);
    $('#image2_clear_div').hide();
});

$(function () {
    $('.selectpicker').selectpicker();
});


$("#image1-clear_id").change(function () {
    if (this.checked) {
        $('#image1_input').hide("slow")
    } else {
        $('#image1_input').show("slow")
    }
});
$("#image2-clear_id").change(function () {
    if (this.checked) {
        $('#image2_input').hide("slow")
    } else {
        $('#image2_input').show("slow")
    }
});
$(".delete_product").click(function (e) {
    var result = confirm('Are you sure to delete this product');
    if (result == true) {
    } else {
        e.preventDefault();
    }
});

})