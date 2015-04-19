$(document).ready(function() {

    $(document).on('click', '.tag', function() {
        var tag = $(this).data('tag-selector');
        if (tag === "all") {
            $('.item').removeClass('hidden');
        } else {
            $('.item').not('.' + tag).addClass('hidden');
            $('.' + tag).removeClass('hidden')
        }

    });

    $(document).on('click', '.delete-item', function() {
        var itemId = $(this).parent().data('id');
        swal({
                title: "Are you sure you'd like to delete this item?",
                text: "",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            },
            function() {
                swal("Deleted!", "Your item has been deleted.", "success");
                delete_item(itemId);
            });
    });

    $(document).on('click', '.check-item', function() {
        var itemId = parseInt($(this).parent().data('id'));
        check(itemId);
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
                $(".item[data-id='" + id + "'] .check-item").removeClass("fa-circle-o").addClass("fa-check-circle-o");
            } else {
                $(".item[data-id='" + id + "'] .check-item").removeClass("fa-check-circle-o").addClass("fa-circle-o");
            }
        },
        error: function(jqXHR) {
            console.log("An ajax error occurred");
            console.log(jqXHR);
        }
    });
}

function delete_item(id) {
    data = {}
    data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    data['item-id'] = id;
    $.ajax({
        url: '/ajax/delete/',
        dataType: 'json',
        method: 'POST',
        data: data,
        success: function(response) {
            if (response.success) {
                $(".item[data-id='" + id + "']").remove();
            }
        }, error: function(jqXHR) {
            console.log("An ajax error occurred");
            console.log(jqXHR);
        }
    })
}

function update_percent(percent) {
    $("#percent-complete-display").html(percent);
    $("#percent-complete-bar").css("width", percent + "%");
    $("#percent-uncomplete-bar").css("width", 100 - percent + "%");
}
