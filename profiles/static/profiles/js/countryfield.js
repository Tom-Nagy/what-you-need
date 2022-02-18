let countrySelected = $('#id_default_country').val();
if (!countrySelected) {
    $('#id_default_country').css('color', '#0d0d0d80');
};
$('#id_default_country').change(function () {
    countrySelected = $(this).val();
    if (!countrySelected) {
        $(this).css('color', '#0d0d0d80');
    } else {
        $(this).css('color', '#0d0d0d');

    }
});