$(document).ready(function () {

  $(document).on('click', '.tag', function () {
    var tag = $(this).data('tag-selector');
    if(tag === "all"){
      $('.item').removeClass('hidden');
    }else{
      $('.item').not('.'+tag).addClass('hidden');
      $('.'+tag).removeClass('hidden')
    }

  })

});

function checkOff(id) {
    data = {};
    data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    data['item-id'] = id;
    $.ajax({
        url: '/ajax/checkoff/',
        dataType: 'json',
        method: 'POST',
        data: data,
        success: function(response) {
            if (response.checked) {
                // TODO check off the thing
            }
        }, error: function(jqXHR) {
            console.log("An ajax error occurred");
            console.log(jqXHR);
        }
    });
}

