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
