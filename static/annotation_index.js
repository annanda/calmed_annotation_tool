function save(checkbox_id) {
    var checkbox = document.getElementById(checkbox_id);
    localStorage.setItem(checkbox_id, checkbox.checked);
}

function load_checkbox() {
    // let checkbox_id = "ED_dataset_makes_sad_small.mp4"
    // let checked = JSON.parse(localStorage.getItem(checkbox_id));
    // let check_elem = document.getElementById(checkbox_id);
    // $(check_elem).prop('checked', checked);
    let elem_id;
    $(".checkboxes").each(function () {
        elem_id = $(this).attr('id');
        let checked = JSON.parse(localStorage.getItem(elem_id));
        let check_elem = document.getElementById(elem_id)
        $(check_elem).prop('checked', checked);
    });
}

window.onload = function () {

    load_checkbox()

    $('.videos_to_annotate_list').click(function () {
        var id_checkbox = $(this).attr('id')
        var checkbox_change = document.getElementById(id_checkbox)
        $(checkbox_change).prop('checked', true);
        save(id_checkbox)
    });

    $('.checkboxes').click(function () {
        var id_checkbox = $(this).attr('id')
        // var checkbox_change = document.getElementById(id_checkbox)
        // $(this).prop('checked', true);
        save(id_checkbox)
    });

}
$(document).on('keypress', ':input:not(textarea):not([type=submit])', function (e) {
    if (e.which == 13) e.preventDefault();
});