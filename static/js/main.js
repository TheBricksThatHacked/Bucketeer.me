
$(document).ready(function () {

  $(document).on('click', '.tag', function () {
  var tag = $(this).data('tag-selector');
  if(tag === "all"){
    $('.item').removeClass('hidden');
  }else{
    $('.item').not('.'+tag).addClass('hidden');
    $('.'+tag).removeClass('hidden')
  }

  });

  $(document).on('click', '.delete-item', function () {
    var itemId = $(this).parent().data('id');
    console.log("Delete Item: " + itemId)
  });
  
  $(".checkbox").click(function() {
    var itemId = $(this).parent().data('id');
    check(parseInt(itemId));
  })

});

function check(id) {
  data = {};
  data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  data['item-id'] = id;
  $.ajax({
    url: '/ajax/check/',
    dataType: 'json',
    method: 'POST',
    data: data,
    success: function(response) {
      if (response.checked) {
        $("#item-" + id).removeClass("fa-circle-o").addClass("fa-check-circle-o");
      } else {
        $("#item-" + id).removeClass("fa-check-circle-o").addClass("fa-circle-o");
      }
    }, error: function(jqXHR) {
      console.log("An ajax error occurred");
      console.log(jqXHR);
    }
  });
}

