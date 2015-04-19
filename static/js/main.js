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
            var checked = $(".item[data-id='" + id + "']").find('i').hasClass('fa-check-circle-o');
            if (response.checked) {
                $(".item[data-id='" + id + "'] .check-item").removeClass("fa-circle-o").addClass("fa-check-circle-o");
            } else {
                $(".item[data-id='" + id + "'] .check-item").removeClass("fa-check-circle-o").addClass("fa-circle-o");
            }
            if (checked) {
                profile_data.complete -= 1;
            }
            else {
                profile_data.complete += 1;
            }
            update_percent(100 * profile_data.complete / profile_data.total);
            $("#items-complete").html(profile_data.complete);
            $("#items-total").html(profile_data.total);
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
            var checked = $(".item[data-id='" + id + "']").find('i').hasClass('fa-check-circle-o');
            if (response.success) {
                $(".item[data-id='" + id + "']").remove();
            }
            if (!profile_data) {
                profile_data = {complete: 0, total: 1} // avoid divide by 0
            }
            if (checked) {
                profile_data.complete -= 1;
            }
            profile_data.total -= 1;
            update_percent(100 * profile_data.complete / profile_data.total);
            $("#items-complete").html(profile_data.complete);
            $("#items-total").html(profile_data.total);
        }, error: function(jqXHR) {
            console.log("An ajax error occurred");
            console.log(jqXHR);
        }
    });
}

function update_percent(percent) {
    $("#percent-complete-display").html(percent);
    $("#percent-complete-bar").css("width", percent + "%");
    $("#percent-uncomplete-bar").css("width", 100 - percent + "%");
}