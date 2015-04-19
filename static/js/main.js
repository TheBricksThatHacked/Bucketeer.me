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
